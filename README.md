# Catppuccin for Claude Code

The four [Catppuccin](https://catppuccin.com) flavors as Claude Code themes. Every color is set except the mascot's.

| Theme | Base |
| --- | --- |
| Catppuccin Latte | light |
| Catppuccin Frappé | dark |
| Catppuccin Macchiato | dark |
| Catppuccin Mocha | dark |

## Install

Needs Claude Code 2.1.118 or later, and 2.1.275 for the one-line install.

At the prompt of a Claude Code terminal session:

```
/plugin install catppuccin --marketplace mkutlak/claude-code-catppuccin
```

Answer `y` to add the marketplace, then pick a scope.

From a shell (2.1.292 or later):

```
claude plugin install catppuccin --marketplace mkutlak/claude-code-catppuccin
```

On an older Claude Code, add the marketplace first:

```
/plugin marketplace add mkutlak/claude-code-catppuccin
/plugin install catppuccin@catppuccin
```

In the desktop app, where `/plugin` does not run: click + next to the prompt box, then Plugins, Add marketplace with `mkutlak/claude-code-catppuccin`, then Add plugin.

## Use

Run `/theme` and pick a flavor, or set it in `settings.json`:

```json
{ "theme": "custom:catppuccin:catppuccin-mocha" }
```

## How the colors are picked

Each token gets the role the [Catppuccin style guide](https://github.com/catppuccin/catppuccin/blob/main/docs/style-guide.md) gives it. Where the guide has no role, or its role does not read well in a terminal:

- Claude's accent is Peach, so Claude stays orange. The mascot keeps Claude Code's own colors.
- Diff backgrounds are built in OKLCH, stepping from Base toward Text. The guide's 20% Green or Red over Base comes out grey, so added and removed lines would look alike.
- Dim text is Overlay 2 (Subtext 0 on Latte), not the guide's Overlay 1, which is too faint on a user message's background.
- Auto-accept and bash mode have no role in the guide, so they keep the hue of Claude Code's own dark theme.

## Changing the themes

The files in `themes/` are generated. Edit the mapping in `tools/gen.py`, then:

```
python3 tools/gen.py
claude plugin validate .
claude --plugin-dir .
```

Bump `version` in `.claude-plugin/plugin.json` when you release a change, or installed copies will not pick it up.

## Credits

Colors from [catppuccin/palette](https://github.com/catppuccin/palette) (MIT).

## License

[MIT](LICENSE)
