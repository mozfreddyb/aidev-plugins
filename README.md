# AI Agent Plugins for Mozilla Developers

This repository is the home for AI agent plugins meant to be used by Mozilla developers. For plugins that are specific to Firefox, please consider [firefox-aidev-plugins](https://github.com/mozilla/firefox-aidev-plugins).

Currently supported agents:

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

As other agents (e.g., Codex) add marketplace support, plugins here will be extended to support them as well.

If you have a plugin that you think would be useful for Mozilla developers, please feel free to open a PR to add it here.

## Installation

From Claude Code, type:

```
/plugin marketplace add mozilla/aidev-plugins
```

## Structure

Plugins are organized in the `plugins/` directory, with each plugin in its own subdirectory. Each plugin must also be listed in `.claude-plugin/marketplace.json` to be discoverable.

```bash
plugins/
├── plugin-name/
│   ├── .claude-plugin/
│   │   └── plugin.json      # Plugin metadata (required)
│   ├── .mcp.json            # MCP server configuration (optional)
│   ├── commands/            # Slash commands (optional)
│   ├── agents/              # Agent definitions (optional)
│   ├── skills/              # Skill definitions (optional)
│   └── README.md            # Documentation
├── another-plugin/
│   └── ...
└── ...
```
