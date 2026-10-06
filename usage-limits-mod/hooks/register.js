// plan limits shown above the prompt. data comes from $.session.usage().rateLimits

// turn a "kind" like five_hour into "5h" / "7d" style labels
function label(kind) {
  const k = String(kind).toLowerCase()
  const m = k.match(/(\d+)[_ ]?(hour|day|week|h|d|w)/)
  if (m) return m[1] + m[2][0]
  return k.replace(/_/g, ' ')
}

// resetsAt may be epoch seconds, epoch ms, or an ISO string
function untilReset(resetsAt) {
  if (resetsAt == null) return ''
  let t = typeof resetsAt === 'number' ? (resetsAt < 1e12 ? resetsAt * 1000 : resetsAt) : Date.parse(resetsAt)
  if (!Number.isFinite(t)) return ''
  const mins = Math.max(0, Math.round((t - Date.now()) / 60000))
  if (mins >= 1440) return Math.floor(mins / 1440) + 'd ' + Math.floor((mins % 1440) / 60) + 'h'
  if (mins >= 60) return Math.floor(mins / 60) + 'h ' + (mins % 60) + 'm'
  return mins + 'm'
}

function bar(pct, width = 10) {
  const filled = Math.round((Math.min(100, Math.max(0, pct)) / 100) * width)
  return '█'.repeat(filled) + '░'.repeat(width - filled)
}

function colorFor(pct) {
  if (pct >= 90) return 'red'
  if (pct >= 70) return 'yellow'
  return 'green'
}

export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'limits', description: 'Show your plan usage limits', immediate: true })
    // reset countdowns tick even when no new usage comes in
    $.clock.every(60000, () => $.ui.invalidate('ui.render'))
    return next(e)
  })

  // fires after each turn and whenever a plan limit's percent changes
  on('session.measure', async ($, e, next) => {
    $.ui.invalidate('ui.render')
    return next(e)
  })

  on('command.run', { command: 'limits' }, async ($) => {
    const { rateLimits } = await $.session.usage()
    if (!rateLimits || rateLimits.length === 0) return { text: 'no plan limit data for this session' }
    const lines = rateLimits.map((r) => {
      const reset = untilReset(r.resetsAt)
      return label(r.kind) + '  ' + bar(r.percentUsed, 20) + '  ' + Math.round(r.percentUsed) + '%' + (reset ? '  resets in ' + reset : '')
    })
    return { text: lines.join('\n') }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const { rateLimits } = await $.session.usage()
    // nothing to show (api key users, or no data yet): leave the band to others
    if (!rateLimits || rateLimits.length === 0) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    const rest = await next(e)
    const items = rateLimits.map((r) => {
      const reset = untilReset(r.resetsAt)
      return Box({
        key: 'limit-' + r.kind,
        flexDirection: 'row',
        columnGap: 1,
        children: [
          Text({ dimColor: true, children: [label(r.kind)] }),
          Text({ color: colorFor(r.percentUsed), children: [bar(r.percentUsed)] }),
          Text({ children: [Math.round(r.percentUsed) + '%'] }),
          ...(reset ? [Text({ dimColor: true, children: ['↻ ' + reset] })] : []),
        ],
      })
    })
    const children = [Box({ key: 'limits-row', flexDirection: 'row', columnGap: 3, children: items })]
    if (rest) children.push(rest)
    return Box({ flexDirection: 'column', children })
  })
}
