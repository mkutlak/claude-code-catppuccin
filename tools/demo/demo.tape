# record.sh replaces @flavor@ and runs this once per flavor.
Output "/out/catppuccin-@flavor@.webm"

# Set lines must come before any other command: VHS ignores them after.
Set Shell bash
Set Theme "catppuccin-@flavor@"
Set FontSize 16
Set Width 1200
Set Height 720
Set Padding 24
Set TypingSpeed 40ms
Set Framerate 25

# Startup screens stay out of the recording. Without COLORTERM, Claude Code rounds to 256 colors.
Hide
Type "cd ~/demo && clear && COLORTERM=truecolor claude --plugin-dir ~/plugin --model haiku --permission-mode default"
Enter
Wait+Screen@30s /❯/
Sleep 1s
Show

Type "Rename greet to welcome in app.py. Only edit the file."
Sleep 500ms
Enter
Wait+Screen@60s /Do you want/
Sleep 3s
Enter
Sleep 1s
Wait+Screen@60s /\d+s · done/
Sleep 2s

Shift+Tab
Sleep 2s
Type "!"
Sleep 1s
Type "ls"
Sleep 500ms
Enter
Sleep 3s
