#!/usr/bin/env bash
# Records /out/catppuccin-<flavor>.webp for each flavor in $FLAVORS, from a clean home.
set -euo pipefail

# Moved off ANTHROPIC_API_KEY so Claude Code reads it through apiKeyHelper and asks no question.
export DEMO_KEY="${ANTHROPIC_API_KEY:?pass the key with --env-file}"
unset ANTHROPIC_API_KEY
export HOME=/tmp/home DISABLE_AUTOUPDATER=1

for flavor in ${FLAVORS:-latte frappe macchiato mocha}; do
  sed "s/@flavor@/$flavor/g" /opt/demo.tape > /tmp/demo.tape
  # Claude's replies and API latency vary, so a take sometimes times out: retry it once from a clean home.
  for take in 1 2; do
    rm -rf "$HOME" && mkdir -p "$HOME/.claude" "$HOME/demo" "$HOME/plugin"
    cp -r /src/.claude-plugin /src/themes "$HOME/plugin/"
    printf '{"theme":"custom:catppuccin:catppuccin-%s","apiKeyHelper":"printenv DEMO_KEY"}\n' "$flavor" > "$HOME/.claude/settings.json"
    printf '{"hasCompletedOnboarding":true,"projects":{"%s":{"hasTrustDialogAccepted":true}}}\n' "$HOME/demo" > "$HOME/.claude.json"
    printf 'def greet(name):\n    return f"Hello, {name}!"\n\n\nprint(greet("world"))\n' > "$HOME/demo/app.py"
    vhs /tmp/demo.tape && break
    [ "$take" = 2 ] && exit 1
    echo "$flavor: take $take failed, retrying" >&2
  done
  # Lossless WebP, not GIF: a GIF's 256 colors wash out the accent colors. bgra makes ffmpeg, not libwebp, convert from YUV.
  ffmpeg -v error -y -i "/out/catppuccin-$flavor.webm" -pix_fmt bgra -c:v libwebp_anim -lossless 1 -loop 0 "/out/catppuccin-$flavor.webp"
  rm "/out/catppuccin-$flavor.webm"
done
