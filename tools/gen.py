#!/usr/bin/env python3
"""Writes themes/catppuccin-<flavor>.json for the four flavors. Run it after changing the mapping below.

Each token gets the role the Catppuccin style guide gives it:
https://github.com/catppuccin/catppuccin/blob/main/docs/style-guide.md
The palettes are github.com/catppuccin/palette (palette.json).
"""
import json
import math
from pathlib import Path

P = {
    "latte": ("Catppuccin Latte", "light", dict(rosewater="#dc8a78", flamingo="#dd7878", pink="#ea76cb", mauve="#8839ef", red="#d20f39", maroon="#e64553", peach="#fe640b", yellow="#df8e1d", green="#40a02b", teal="#179299", sky="#04a5e5", sapphire="#209fb5", blue="#1e66f5", lavender="#7287fd", text="#4c4f69", subtext1="#5c5f77", subtext0="#6c6f85", overlay2="#7c7f93", overlay1="#8c8fa1", overlay0="#9ca0b0", surface2="#acb0be", surface1="#bcc0cc", surface0="#ccd0da", base="#eff1f5", mantle="#e6e9ef", crust="#dce0e8")),
    "frappe": ("Catppuccin Frappé", "dark", dict(rosewater="#f2d5cf", flamingo="#eebebe", pink="#f4b8e4", mauve="#ca9ee6", red="#e78284", maroon="#ea999c", peach="#ef9f76", yellow="#e5c890", green="#a6d189", teal="#81c8be", sky="#99d1db", sapphire="#85c1dc", blue="#8caaee", lavender="#babbf1", text="#c6d0f5", subtext1="#b5bfe2", subtext0="#a5adce", overlay2="#949cbb", overlay1="#838ba7", overlay0="#737994", surface2="#626880", surface1="#51576d", surface0="#414559", base="#303446", mantle="#292c3c", crust="#232634")),
    "macchiato": ("Catppuccin Macchiato", "dark", dict(rosewater="#f4dbd6", flamingo="#f0c6c6", pink="#f5bde6", mauve="#c6a0f6", red="#ed8796", maroon="#ee99a0", peach="#f5a97f", yellow="#eed49f", green="#a6da95", teal="#8bd5ca", sky="#91d7e3", sapphire="#7dc4e4", blue="#8aadf4", lavender="#b7bdf8", text="#cad3f5", subtext1="#b8c0e0", subtext0="#a5adcb", overlay2="#939ab7", overlay1="#8087a2", overlay0="#6e738d", surface2="#5b6078", surface1="#494d64", surface0="#363a4f", base="#24273a", mantle="#1e2030", crust="#181926")),
    "mocha": ("Catppuccin Mocha", "dark", dict(rosewater="#f5e0dc", flamingo="#f2cdcd", pink="#f5c2e7", mauve="#cba6f7", red="#f38ba8", maroon="#eba0ac", peach="#fab387", yellow="#f9e2af", green="#a6e3a1", teal="#94e2d5", sky="#89dceb", sapphire="#74c7ec", blue="#89b4fa", lavender="#b4befe", text="#cdd6f4", subtext1="#bac2de", subtext0="#a6adc8", overlay2="#9399b2", overlay1="#7f849c", overlay0="#6c7086", surface2="#585b70", surface1="#45475a", surface0="#313244", base="#1e1e2e", mantle="#181825", crust="#11111b")),
}


def mix(top, bottom, a):
    """top at opacity a over bottom: the guide's "Green (20% opacity)" is mix(green, base, .2)."""
    rgb = lambda h: [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(t * a + b * (1 - a)) for t, b in zip(rgb(top), rgb(bottom)))


# Sanity check for mix(): Catppuccin's own delta port uses these two for Mocha's added lines.
assert mix("#a6e3a1", "#1e1e2e", .2) == "#394545" and mix("#a6e3a1", "#1e1e2e", .35) == "#4e6356"


def lightness(h):
    """OKLab L of a hex color."""
    r, g, b = (v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)))
    l, m, s = ((.4122214708 * r + .5363325363 * g + .0514459929 * b) ** (1 / 3),
               (.2119034982 * r + .6806995451 * g + .1073969566 * b) ** (1 / 3),
               (.0883024619 * r + .2817188376 * g + .6299787005 * b) ** (1 / 3))
    return .2104542553 * l + .7936177850 * m - .0040720468 * s


def lch(L, C, H):
    """OKLCH to hex. Asserts the color fits sRGB, so nothing is clipped into a different hue."""
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l, m, s = (L + .3963377774 * a + .2158037573 * b) ** 3, (L - .1055613458 * a - .0638541728 * b) ** 3, (L - .0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + .2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - .3413193965 * s,
           -.0041960863 * l - .7034186147 * m + 1.7076147010 * s)
    assert all(-.001 <= v <= 1.001 for v in rgb), f"lch({L:.3f}, {C}, {H}) is outside sRGB"
    enc = lambda v: round(255 * (12.92 * v if v <= .0031308 else 1.055 * v ** (1 / 2.4) - .055))
    return "#%02x%02x%02x" % tuple(enc(min(max(v, 0), 1)) for v in rgb)


def overrides(c, light):
    base_l, text_l = lightness(c["base"]), lightness(c["text"])
    tint = lambda hue, step, chroma: lch(base_l + step * (text_l - base_l), chroma, hue)
    # Shimmer is the lighter half of a spinner gradient: the guide's "60% Text/<color> mix",
    # read as 60% of the color so the hue stays (60% Text washes peach out to grey).
    # Latte's Text is dark, so there the lighter half comes from Base.
    shimmer = lambda k: mix(c[k], c["base" if light else "text"], .6)
    # The guide's Subtle (Overlay 1) is 2.8-3.4:1 on a user message; Overlay 2 is the comment colour of the
    # nvim and vscode ports. Latte's Overlay 2 is still 2.6:1 there, so Latte steps up to Subtext 0.
    dim = "subtext0" if light else "overlay2"
    return [
        {  # Typography
            "text": c["text"],               # Body Copy
            "inverseText": c["base"],        # On Accent
            "inactive": c[dim],
            "inactiveShimmer": shimmer(dim),
            "subtle": c["overlay0"],         # Inactive Border
            "suggestion": c["lavender"],     # Active Line Number: the highlighted entry
            "permission": c["lavender"],     # Active Border
            "permissionShimmer": shimmer("lavender"),
            "remember": c["blue"],           # Tags, Pills
        },
        {  # Accent: Catppuccin ports let the user pick one; peach keeps Claude's orange.
            "claude": c["peach"],
            "claudeShimmer": shimmer("peach"),
            "briefLabelClaude": c["peach"],
            "briefLabelYou": c["blue"],      # Tags, Pills
            # clawd_body and clawd_background are left to Claude Code: in Peach the mascot looks washed out.
        },
        {
            "success": c["green"],
            "error": c["red"],
            "warning": c["yellow"],
            "warningShimmer": shimmer("yellow"),
            "merged": c["mauve"],
        },
        {  # Modes: no role in the guide, so each keeps the hue of Claude Code's own dark preset.
            "promptBorder": c["overlay0"],   # Inactive Border: the box is always there, dialogs are the active ones
            "promptBorderShimmer": shimmer("overlay0"),
            "planMode": c["teal"],           # Information
            "autoAccept": c["mauve"],
            "autoAcceptShimmer": shimmer("mauve"),
            "bashBorder": c["pink"],
            "ide": c["sapphire"],
            "fastMode": c["peach"],
            "fastModeShimmer": shimmer("peach"),
            "effortUltra": c["mauve"],
            "skill": c["mauve"],
            "claudeBlue_FOR_SYSTEM_SPINNER": c["lavender"],
            "claudeBlueShimmer_FOR_SYSTEM_SPINNER": shimmer("lavender"),
            "background": c["teal"],
            "chromeYellow": c["yellow"],
            "professionalBlue": c["sapphire"],
        },
        {  # Diff & Merge: the guide's 15-25% mix over a blue-violet Base comes out grey, so add and remove look alike
            # (and land on the same grey at 256 colors). Built in OKLCH instead: Base's lightness stepped toward Text
            # (line, word on top of it, dimmed below), at a real chroma. Hues sit a touch off the palette's green (143)
            # and red (3) so the tints read as green and red, not olive and pink.
            "diffAdded": tint(150, .215, .065),
            "diffAddedWord": tint(150, .33, .09),
            "diffAddedDimmed": tint(150, .11, .04),
            "diffRemoved": tint(10, .215, .075),
            "diffRemovedWord": tint(10, .33, .10),
            "diffRemovedDimmed": tint(10, .11, .045),
        },
        {  # Surface Elements
            "userMessageBackground": c["surface0"],
            "userMessageBackgroundHover": c["surface1"],
            "bashMessageBackgroundColor": c["surface0"],
            "memoryBackgroundColor": c["surface0"],
            "composerSidebarBackground": c["mantle"],  # Sidebars are Mantle in the vscode and nvim ports
            # The guide's Overlay 2 at 20-30% vanishes over a Surface 0 message; legibility first.
            "selectionBg": c["surface2"],
        },
        {
            "rate_limit_fill": c["blue"],
            "rate_limit_empty": c["surface1"],
        },
        # Terminal colors: purple is Mauve, orange is Peach (color16), cyan is Teal (color6).
        {f"{n}_FOR_SUBAGENTS_ONLY": c[k] for n, k in [("red", "red"), ("blue", "blue"), ("green", "green"), ("yellow", "yellow"), ("purple", "mauve"), ("orange", "peach"), ("pink", "pink"), ("cyan", "teal")]},
        # Rainbow Highlights: Red, Peach, Yellow, Green, Sapphire, Lavender; Mauve is the seventh, violet.
        {f"rainbow_{n}{s}": (shimmer(k) if s else c[k]) for n, k in [("red", "red"), ("orange", "peach"), ("yellow", "yellow"), ("green", "green"), ("blue", "sapphire"), ("indigo", "lavender"), ("violet", "mauve")] for s in ("", "_shimmer")},
    ]


out = Path(__file__).resolve().parent.parent / "themes"
for slug, (name, base, c) in P.items():
    groups = [",\n".join(f"    {json.dumps(k)}: {json.dumps(v)}" for k, v in g.items()) for g in overrides(c, base == "light")]
    body = ",\n\n".join(groups)
    (out / f"catppuccin-{slug}.json").write_text(f'{{\n  "name": {json.dumps(name, ensure_ascii=False)},\n  "base": "{base}",\n  "overrides": {{\n{body}\n  }}\n}}\n', encoding="utf-8")
    print(f"wrote {out.name}/catppuccin-{slug}.json")
