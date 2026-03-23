# CMake Build Flags

RediSearch uses CMake as its primary build system. The spec passes these flags
via the `%cmake` RPM macro, which also adds standard Fedora compiler flags,
install prefix, and library paths automatically.

## Flags

### -DCOORD_TYPE=oss

RediSearch has two build modes:

- `oss` — open-source standalone module
- `rlec` — Redis Enterprise cluster coordination

We build the standalone version.

### -DBOOST_DIR=%{_includedir}

Tells CMake to find Boost headers from the system (`/usr/include`) rather than
downloading or bundling its own copy. This is how we use Fedora's `boost-devel`
instead of bundling Boost.

### -DREDISEARCH_BUILD_SHARED=ON

Builds `redisearch.so` as a shared library (a Redis module `.so` file). Without
this, the build produces a static library that Redis cannot load.

### -DBUILD_SEARCH_UNIT_TESTS=OFF

Disables compilation of RediSearch's unit tests. They're not needed in a
package build and pull in extra test-only dependencies.

### -DVECSIM_BUILD_TESTS=OFF

Same as above, for VectorSimilarity's test suite.

### -DUSE_SVS=OFF

Disables Intel SVS (Scalable Vector Search). SVS is an Intel-specific SIMD
library that is not packaged for Fedora and only works on x86 CPUs with
specific instruction set extensions. This is also why we need the SVS header
guard patch (see `docs/patches.md`).

### -DFETCHCONTENT_SOURCE_DIR_CPU_FEATURES=$PWD/cpu_features-0.10.1

CMake's `FetchContent` mechanism would normally download `cpu_features` from
GitHub during the build. This flag redirects it to the copy extracted from
`Source2` during `%prep`, avoiding any network access. The upstream tarball
is fetched by `spectool -g` (or `make download`) alongside the other sources.

### -DFETCHCONTENT_FULLY_DISCONNECTED=ON

A CMake-wide flag that prevents `FetchContent` from attempting **any** network
downloads. If any dependency tries to fetch something we haven't provided, the
build fails immediately instead of hanging or silently downloading. Required
for mock and COPR builds which may not have network access.

### -DRUST_PROFILE=release

Builds the Rust components (`src/redisearch_rs/`) with release optimizations.
Without this it defaults to debug profile, which produces slower and larger
binaries.
