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

# Strip the GPL-2.0 kernel-module test fixture shipped by the ``nix`` crate.
# It is unreachable from the released ``redisearch.so`` (it lives under
# ``vendor/nix/test/test_kmod/`` and is only compiled by the crate's test
# suite). Removing it here keeps fedora-review's licensecheck quiet without
# any %%prep mutation in the spec, and we update ``.cargo-checksum.json`` so
# the offline ``cargo build`` in the buildroot still passes integrity checks.
NIX_VENDORED="$DEST/vendor/nix"
if [ -f "$NIX_VENDORED/test/test_kmod/hello_mod/hello.c" ] &&
   [ -f "$NIX_VENDORED/.cargo-checksum.json" ]; then
    echo "==> Stripping GPL-2.0 nix kernel-module test fixture from Source0"
    rm -f "$NIX_VENDORED/test/test_kmod/hello_mod/hello.c"
    python3 - "$NIX_VENDORED/.cargo-checksum.json" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
d = json.loads(p.read_text())
d["files"].pop("test/test_kmod/hello_mod/hello.c", None)
p.write_text(json.dumps(d))
PY
fi

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
