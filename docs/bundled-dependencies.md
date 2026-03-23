# Bundled Dependencies

Fedora discourages bundling — the preferred approach is to use system packages.
When bundling is unavoidable, `Provides: bundled(...)` declarations are
**required** so Fedora can track what's embedded and flag security issues.

RediSearch has a large number of bundled declarations.  Most of them are
misleading at first glance — they fall into different categories with different
justifications.

## Categories

### Rust workspace crates (~30 entries)

```
Provides: bundled(crate(buffer)) = 0.0.1+git...
Provides: bundled(crate(document)) = 0.0.1+git...
...
```

These are **RediSearch's own source code** split into a Rust workspace, not
third-party libraries.  They're all version `0.0.1` and live under
`src/redisearch_rs/`.  Fedora Rust packaging guidelines require declaring
them as `bundled(crate(...))`, which makes the list look much larger than it
really is.  There is nothing to unbundle here.

### C/C++ in-tree libraries (~10 entries)

```
Provides: bundled(snowball) = 2.1.0
Provides: bundled(friso) = 1.6.2
Provides: bundled(fast_float) = 7.0.0
...
```

Small, niche libraries embedded directly in the source tree, often with
RediSearch-specific modifications.  Most are **not packaged in Fedora** at all
(snowball stemmer, friso segmenter, cndict, phonetics, etc.), so there is
nothing to unbundle against.

### Git submodule dependencies (~6 entries)

```
Provides: bundled(hiredis) = 1.0.2~git...
Provides: bundled(VectorSimilarity) = 0.8~git...
Provides: bundled(s2geometry) = 0.10.0~git...
Provides: bundled(cpu_features) = 0.10.1
Provides: bundled(RedisModulesSDK) = 0~git...
Provides: bundled(libuv) = 1.48.0~git...
```

This is the **real bundling concern**.  These are substantial libraries pulled
in as git submodules.  RediSearch's CMake build compiles them directly and does
not support linking against system versions.

### Rust git dependencies (2 entries)

```
Provides: bundled(crate(redis-module)) = 99.99.99+git...
Provides: bundled(crate(redis-module-macros-internals)) = 99.99.99+git...
```

The `redismodule-rs` crate is pulled from a pinned git revision (not published
on crates.io).  It's vendored alongside the other Rust crates.

## What already uses system packages

- **Boost** — linked against Fedora's `boost-devel`
- **OpenSSL** — linked against Fedora's `openssl-devel`

## What could realistically be unbundled

| Library | Fedora package | Blocker |
|---------|---------------|---------|
| hiredis | `hiredis-devel` | RediSearch pins a specific version/fork; build system doesn't support system hiredis |
| s2geometry | `s2geometry-devel` | Version compatibility not verified; build system compiles its own copy |
| libuv | `libuv-devel` | Same — pinned version, compiled in-tree |

Unbundling any of these requires upstream CMake changes to support finding and
linking against system-installed versions.

## What cannot be unbundled

- **VectorSimilarity** — RediSearch-specific library, not independently packaged
- **RedisModulesSDK** — Redis module development headers, bundled by design
- **cpu_features** — small Google library, not in Fedora; used only by VectorSimilarity
- **In-tree C/C++ libs** — tightly integrated, often modified, not in Fedora
- **Rust workspace crates** — RediSearch's own code, not third-party
