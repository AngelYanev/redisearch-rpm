#!/bin/bash
# Create the RediSearch source tarball from a local checkout.
# Includes git submodules, downloads cpu_features, and cleans up
# macOS resource forks so the spec %prep stays minimal.
#
# Usage: ./makesrc.sh /path/to/RediSearch

set -euo pipefail

SRCDIR="${1:?Usage: $0 /path/to/RediSearch}"
NAME=$(basename "$PWD")
PROJECT=$(sed -n '/^%global gh_proj/{s/.* //;p}' "$NAME.spec")
UPSTREAM=$(awk '/^%global upstream_version /{print $3; exit}' "$NAME.spec")
CPU_FEATURES_VER=$(sed -n 's|.*cpu_features-\([0-9.]*\)\.tar\.gz.*|\1|p' "$NAME.spec")
DEST="$PROJECT-$UPSTREAM"

echo "==> Copying source tree"
rm -rf "$DEST"
cp -a "$SRCDIR" "$DEST"

echo "==> Cleaning VCS and macOS metadata"
find "$DEST" -name '.git' -prune -exec rm -rf {} + 2>/dev/null || true
find "$DEST" -name '._*' -delete

echo "==> Creating .git marker for Rust build_utils::git_root()"
mkdir -p "$DEST/.git"

if [ -n "$CPU_FEATURES_VER" ]; then
    echo "==> Downloading cpu_features v$CPU_FEATURES_VER"
    curl -fsSL "https://github.com/google/cpu_features/archive/refs/tags/v${CPU_FEATURES_VER}.tar.gz" |
        tar xz -C "$DEST"
fi

echo "==> Archiving $NAME-$UPSTREAM.tgz (matches %%global upstream_version in spec)"
tar czf "$NAME-$UPSTREAM.tgz" "$DEST"

echo "==> Cleaning"
rm -rf "$DEST"

echo "Done: $NAME-$UPSTREAM.tgz"
