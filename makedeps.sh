#!/bin/bash
# Create vendored Rust dependencies tarball from the main source archive.
# Produces: <name>-vendor-<upstream_version>.tgz (see %%global upstream_version) with mycargo/,
# .cargo/config.toml, and rust-vendor-licenses.txt.
# Requires: makesrc.sh to have been run first (or the source tgz to exist).
# Usage: ./makedeps.sh

NAME=$(basename "$PWD")
PROJECT=$(sed -n '/^%global gh_proj/{s/.* //;p}' "$NAME.spec")
UPSTREAM=$(awk '/^%global upstream_version /{print $3; exit}' "$NAME.spec")

if [ ! -f "$NAME-$UPSTREAM.tgz" ]; then
    echo "$NAME-$UPSTREAM.tgz missing — run makesrc.sh first"
    exit 1
fi

echo "+ Unpack"
tar xf "$NAME-$UPSTREAM.tgz"

pushd "$PROJECT-$UPSTREAM" || exit 1

echo "+ Vendor Rust crates"
cargo vendor --manifest-path src/redisearch_rs/Cargo.toml mycargo

# Strip the GPL-2.0 kernel-module test fixture shipped by the ``nix`` crate.
# Same rationale as in makesrc.sh — keep fedora-review's licensecheck quiet
# without any %%prep mutation in the spec; update ``.cargo-checksum.json`` so
# the offline ``cargo build`` in the buildroot still passes integrity checks.
NIX_VENDORED="mycargo/nix"
if [ -f "$NIX_VENDORED/test/test_kmod/hello_mod/hello.c" ] &&
   [ -f "$NIX_VENDORED/.cargo-checksum.json" ]; then
    echo "+ Strip GPL-2.0 nix kernel-module test fixture"
    rm -f "$NIX_VENDORED/test/test_kmod/hello_mod/hello.c"
    python3 - "$NIX_VENDORED/.cargo-checksum.json" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
d = json.loads(p.read_text())
d["files"].pop("test/test_kmod/hello_mod/hello.c", None)
p.write_text(json.dumps(d))
PY
fi

echo "+ Write cargo vendor config"
mkdir -p .cargo
cargo vendor --manifest-path src/redisearch_rs/Cargo.toml mycargo 2>/dev/null |
    sed -n '/^\[source/,$ p' > .cargo/config.toml

echo "+ Generate license manifest"
pushd src/redisearch_rs || exit 1
cargo tree --workspace --offline --edges=normal --no-dedupe \
    --prefix=none --format '{p} | {l}' 2>/dev/null |
    grep -v '(/' | grep -v '| $' | sort -u \
    > ../../rust-vendor-licenses.txt ||
    echo "# vendor license manifest unavailable" > ../../rust-vendor-licenses.txt
popd

echo "+ Pack"
tar czf "../$NAME-vendor-$UPSTREAM.tgz" mycargo .cargo/config.toml rust-vendor-licenses.txt
popd

echo "+ Cleaning"
rm -rf "$PROJECT-$UPSTREAM"

echo "Done: $NAME-vendor-$UPSTREAM.tgz"
