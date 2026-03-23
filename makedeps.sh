#!/bin/bash
# Create vendored Rust dependencies tarball from the main source archive.
# Produces: <name>-deps-<version>.tgz containing mycargo/ (vendored crates
# with .cargo/config.toml) and rust-vendor-licenses.txt.
# Requires: makesrc.sh to have been run first (or the source tgz to exist).
# Usage: ./makedeps.sh

NAME=$(basename "$PWD")
PROJECT=$(sed -n '/^%global gh_proj/{s/.* //;p}' "$NAME.spec")
VERSION=$(sed -n '/^Version:/{s/.* //;p}' "$NAME.spec")

if [ ! -f "$NAME-$VERSION.tgz" ]; then
    echo "$NAME-$VERSION.tgz missing — run makesrc.sh first"
    exit 1
fi

echo "+ Unpack"
tar xf "$NAME-$VERSION.tgz"

pushd "$PROJECT-$VERSION" || exit 1

echo "+ Vendor Rust crates"
cargo vendor --manifest-path src/redisearch_rs/Cargo.toml mycargo

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
tar czf "../$NAME-deps-$VERSION.tgz" mycargo .cargo/config.toml rust-vendor-licenses.txt
popd

echo "+ Cleaning"
rm -rf "$PROJECT-$VERSION"

echo "Done: $NAME-deps-$VERSION.tgz"
