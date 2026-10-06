# usage-limits-mod

Claude plugin hook for T3 Code to display plan usage limits above the prompt and add a `/limits` command.

## features

- Hooks into Claude UI to display active usage limits directly above the prompt box.
- Adds `/limits` command to inspect remaining query quotas and reset times.

## files

- `.claude-plugin/plugin.json`: Plugin manifest defining the hook metadata.
- `hooks/register.js`: Hook registration script.
- `hooks/hooks.json`: Event hooks mapping.
