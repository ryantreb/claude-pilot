#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PILOT_BIN="$HOME/.pilot/bin"
PLUGIN_DIR="$HOME/.claude/pilot"

echo "Installing Claude Pilot Free..."
echo ""

# 1. Remove compiled Cython binary
if ls "$PILOT_BIN"/pilot.cpython-*.so 1>/dev/null 2>&1; then
    rm -f "$PILOT_BIN"/pilot.cpython-*.so
    echo "  [x] Removed Cython binary"
else
    echo "  [-] No Cython binary found (already removed)"
fi

# 2. Rename original shell wrapper if it exists as a file (not directory)
if [ -f "$PILOT_BIN/pilot" ] && [ ! -d "$PILOT_BIN/pilot" ]; then
    mv "$PILOT_BIN/pilot" "$PILOT_BIN/pilot-original.sh"
    echo "  [x] Saved original wrapper as pilot-original.sh"
fi

# 3. Create pilot Python package directory
mkdir -p "$PILOT_BIN/pilot"
for f in __init__.py cli.py context.py license.py plan.py session.py worktree.py statusline_cmd.py; do
    if [ -f "$SCRIPT_DIR/launcher/$f" ]; then
        cp "$SCRIPT_DIR/launcher/$f" "$PILOT_BIN/pilot/$f"
    else
        echo "  [!] Warning: launcher/$f not found in source"
    fi
done
echo "  [x] Installed CLI package to $PILOT_BIN/pilot/"

# 4. Create new shell wrapper
cat > "$PILOT_BIN/pilot-run" << 'WRAPPER'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec uv run --python 3.12 --no-project python -c "
import sys, os
sys.path.insert(0, '${SCRIPT_DIR}')
from pilot import app
code = app()
sys.stdout.flush()
sys.stderr.flush()
os._exit(code)
" "$@"
WRAPPER
chmod +x "$PILOT_BIN/pilot-run"
echo "  [x] Created pilot-run wrapper"

# 5. Update settings to reference pilot-run instead of pilot
SETTINGS_FILE="$HOME/.claude/settings.local.json"
if [ -f "$SETTINGS_FILE" ]; then
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
# Fix statusline command
sl = data.get('statusLine', {})
if 'command' in sl:
    sl['command'] = sl['command'].replace('/.pilot/bin/pilot ', '/.pilot/bin/pilot-run ')
    data['statusLine'] = sl
# Fix env var if present
env = data.get('env', {})
if 'CLAUDE_CODE_STATUSLINE' in env:
    env['CLAUDE_CODE_STATUSLINE'] = env['CLAUDE_CODE_STATUSLINE'].replace(
        '/.pilot/bin/pilot ', '/.pilot/bin/pilot-run '
    )
    data['env'] = env
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && echo "  [x] Updated settings.local.json" || echo "  [-] Could not update settings (manual update may be needed)"
    fi
fi

# 6. Stub license file
cat > "$HOME/.pilot/.license" << 'LICENSE'
{"state":{"license_key":"free","tier":"free","email":"","last_validated_at":null,"activations_used":0},"signature":""}
LICENSE
echo "  [x] Created free license stub"

# 7. Patch hooks that reference the pilot binary
HOOKS_DIR="$HOME/.claude/pilot/hooks"
if [ -f "$HOOKS_DIR/session_end.py" ]; then
    sed -i 's|"pilot-run"|"pilot-run"|; s|/ "bin" / "pilot"|/ "bin" / "pilot-run"|' "$HOOKS_DIR/session_end.py" 2>/dev/null
    # More reliable: replace the exact line
    python3 -c "
p = '$HOOKS_DIR/session_end.py'
with open(p) as f:
    content = f.read()
content = content.replace(
    '/ \".pilot\" / \"bin\" / \"pilot\"',
    '/ \".pilot\" / \"bin\" / \"pilot-run\"'
)
with open(p, 'w') as f:
    f.write(content)
" 2>/dev/null && echo "  [x] Patched session_end.py to use pilot-run" || echo "  [-] Could not patch session_end.py (manual fix needed)"
fi

# 8. Copy deminified JS services if available
if [ -d "$SCRIPT_DIR/pilot/scripts" ]; then
    for f in "$SCRIPT_DIR/pilot/scripts/"*.cjs; do
        [ -f "$f" ] && cp "$f" "$PLUGIN_DIR/scripts/"
    done
    echo "  [x] Updated JS services (deminified, license check removed)"
fi

echo ""
echo "Installation complete!"
echo ""
echo "The CLI is now at: $PILOT_BIN/pilot-run"
echo ""
echo "To make 'pilot' work everywhere, add to your shell profile:"
echo "  alias pilot='$PILOT_BIN/pilot-run'"
echo ""
echo "Or update hooks that call 'pilot' to use 'pilot-run' instead."
