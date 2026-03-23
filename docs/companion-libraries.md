# Companion Shared Libraries & RPM Filters

## Problem

`redisearch.so` dynamically links against several shared libraries that are
built from RediSearch's own source tree:

- `libVectorSimilarity.so` (+ Spaces variants)
- `libhiredis.so.1` / `libhiredis_ssl.so.1`
- `libcpu_features.so`

These are **not** system packages — no Fedora repo provides them. They're
private bundled libraries installed alongside `redisearch.so` in the Redis
modules directory and found at runtime via `RPATH=$ORIGIN`.

RPM's automatic dependency scanner doesn't know this. It scans every `.so` in
the package and:

1. Adds their linked libraries as `Requires:` — so `dnf install redisearch`
   would fail with "nothing provides libVectorSimilarity.so".
2. Advertises the installed `.so` files as `Provides:` — so other packages
   could accidentally depend on our private libraries.

## Current Solution

Two RPM macros in the spec filter out these private libraries:

```rpm
# Don't auto-require our private bundled libs
%global __requires_exclude ^lib(VectorSimilarity|VectorSimilaritySpaces|VectorSimilaritySpaces_no_optimization|cpu_features|hiredis|hiredis_ssl)\.so

# Don't advertise anything in the modules dir as a system-level provider
%global __provides_exclude_from ^%{redis_modules_dir}/.*$
```

The companion `.so` files are installed next to `redisearch.so` and each gets
`RPATH=$ORIGIN` via `patchelf` so the dynamic linker finds them without system
library paths.

## Alternatives

### 1. Static linking (best long-term fix)

If VectorSimilarity, hiredis, and cpu_features were linked statically into
`redisearch.so`, there would be no companion `.so` files at all. This
eliminates:

- The `__requires_exclude` / `__provides_exclude_from` filters
- The companion library install logic in `%install`
- The `patchelf --set-rpath` calls
- The `patchelf` BuildRequires

This is what redis-bloom and redis-json achieve — a single `.so` with no
companions. It requires upstream CMake changes (e.g., building the subprojects
with `BUILD_SHARED_LIBS=OFF`).

### 2. Use system hiredis

Fedora ships `hiredis` and `hiredis-devel`. If RediSearch linked against the
system version instead of bundling its own, we could replace the hiredis filter
entries with `Requires: hiredis`. However, the bundled version (1.0.2) may
differ from Fedora's and could carry Redis-specific patches.

### 3. Private library directory with ld.so.conf

Install companion libs in `/usr/lib64/redisearch/` and add an `ld.so.conf.d`
snippet. More complex and unusual for a Redis module — no real advantage over
the `$ORIGIN` RPATH approach.
