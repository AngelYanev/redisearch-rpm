# remirepo/fedora spec file for redisearch
#
# SPDX-FileCopyrightText: Copyright 2026 Angel Yanev
# SPDX-License-Identifier: MIT
#
#

# Upstream RediSearch sources and release tarballs (makesrc/makedeps tag v plus %%global upstream_version).
%global upstream_version 8.6.0

%global cfgname search.conf
%global libname redisearch.so
%global redis_modules_dir %{_libdir}/redis/modules
%global redis_modules_cfg %{_sysconfdir}/redis/modules
# Github forge
%global gh_vend RediSearch
%global gh_proj RediSearch
%global forgeurl https://github.com/%{gh_vend}/%{gh_proj}

Name:           redisearch
Version:        1.0.0
Release:        1%{?dist}
Summary:        Full-text search, vector similarity, and secondary indexing for Redis

# License breakdown:
#   Upstream RediSearch (Source0): AGPL-3.0-only.
#   Bundled C/C++ submodules (Source0 ``deps/``): MIT (RedisModulesSDK,
#     hiredis, libuv), Apache-2.0 (s2geometry, VectorSimilarity wrappers),
#     BSD-3-Clause (snowball, friso), Zlib (miniz), BSL-1.0 (eve),
#     ISC (cndict locale data), MIT (rmutil, thpool, geohash, fast_float,
#     phonetics, nunicode), Apache-2.0 (cpu_features).
#   Bundled FetchContent C++ deps (Source3..Source7): BSL-1.0 (eve),
#     MIT (robin-map, fmt, spdlog), MIT (tomlplusplus).
#   Vendored Rust crates (Source1) cover the remaining SPDX terms below;
#     aggregated for the binary shared library in %%files. Per-crate detail is
#     in rust-vendor-licenses.txt (installed as %%license).
#   The "Apache-2.0 WITH LLVM-exception" leg covers ``rustix``,
#     ``linux-raw-sys``, ``wasi``, and ``wit-bindgen`` vendored crates.
#   Test-only kernel-module fixture in vendor/nix (GPL-2.0 ``hello.c``) is
#     stripped from the Source0/Source1 tarballs by makesrc.sh/makedeps.sh,
#     not shipped in the binary; GPL-2.0 is not listed.
License:        AGPL-3.0-only AND MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND Zlib AND 0BSD AND BSL-1.0 AND Unicode-DFS-2016 AND Unlicense AND MPL-2.0 AND (Apache-2.0 WITH LLVM-exception)
URL:            %{forgeurl}

# Source tarball includes git submodules (created by makesrc.sh)
Source0:        https://github.com/AngelYanev/redisearch-rpm/releases/download/v%{upstream_version}/%{name}-%{upstream_version}.tar.gz
# Vendored Rust crates + .cargo/config.toml + license manifest (created by makedeps.sh)
Source1:        https://github.com/AngelYanev/redisearch-rpm/releases/download/v%{upstream_version}/%{name}-vendor-%{upstream_version}.tar.gz
# google/cpu_features — required by VectorSimilarity, fetched at build time upstream
Source2:        https://github.com/google/cpu_features/archive/refs/tags/v0.10.1.tar.gz#/cpu_features-0.10.1.tar.gz
# ScalableVectorSearch FetchContent deps — bundled for offline builds
Source3:        https://github.com/jfalcou/eve/archive/refs/tags/v2023.02.15.tar.gz#/eve-2023.02.15.tar.gz
Source4:        https://github.com/Tessil/robin-map/archive/refs/tags/v1.4.0.tar.gz#/robin-map-1.4.0.tar.gz
Source5:        https://github.com/fmtlib/fmt/archive/refs/tags/11.2.0.tar.gz#/fmt-11.2.0.tar.gz
Source6:        https://github.com/gabime/spdlog/archive/refs/tags/v1.15.3.tar.gz#/spdlog-1.15.3.tar.gz
Source7:        https://github.com/marzer/tomlplusplus/archive/refs/tags/v3.3.0.tar.gz#/tomlplusplus-3.3.0.tar.gz

# Private bundled shared libs live alongside redisearch.so — filter them out
# of auto-generated RPM requires/provides so they don't leak as system deps.
%global __requires_exclude ^lib(VectorSimilarity|VectorSimilaritySpaces|VectorSimilaritySpaces_no_optimization|cpu_features|hiredis|hiredis_ssl|fmt|spdlog)\\.so
%global __provides_exclude_from ^%{redis_modules_dir}/.*$

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cmake >= 3.13
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  openssl-devel
BuildRequires:  rust >= 1.80
BuildRequires:  cargo
BuildRequires:  rust-packaging
%if 0%{?fedora} || 0%{?rhel} >= 9
BuildRequires:  cargo-rpm-macros >= 24
%endif
BuildRequires:  boost-devel >= 1.83
BuildRequires:  clang-devel
BuildRequires:  patchelf

# Registry crates that Fedora also ships as rust-*-devel (policy / licensing cross-check).
# The build still uses ``Source1`` vendor offline. Refresh from this dir:
# ``python3 ../../scripts/fedora_crate_audit.py ../../RediSearch/src/redisearch_rs/Cargo.lock --out-dir .``
# then replace the ``rust-*`` block below with ``fedora-buildrequires.inc``.
# Omit ``rust-nix*`` from %%BuildRequires — COPR/mock often cannot resolve those names; crate ``nix`` is vendored and listed under ``bundled(crate(nix))`` below.
BuildRequires:  rust-addr2line-devel
BuildRequires:  rust-adler2-devel
BuildRequires:  rust-aho-corasick-devel
BuildRequires:  rust-anstream0.6-devel
BuildRequires:  rust-anstyle-parse-devel
BuildRequires:  rust-anstyle-query-devel
BuildRequires:  rust-autocfg-devel
BuildRequires:  rust-backtrace-devel
BuildRequires:  rust-base64-devel
BuildRequires:  rust-bindgen-devel
BuildRequires:  rust-bitflags1-devel
BuildRequires:  rust-bumpalo-devel
BuildRequires:  rust-byteorder-devel
BuildRequires:  rust-bytes-devel
BuildRequires:  rust-cast-devel
BuildRequires:  rust-cbindgen-devel
BuildRequires:  rust-cexpr-devel
BuildRequires:  rust-cfg-if-devel
BuildRequires:  rust-ciborium-devel
BuildRequires:  rust-ciborium-io-devel
BuildRequires:  rust-ciborium-ll-devel
BuildRequires:  rust-clang-sys-devel
BuildRequires:  rust-colorchoice-devel
BuildRequires:  rust-crc32fast-devel
BuildRequires:  rust-crossbeam-deque-devel
BuildRequires:  rust-crossbeam-epoch-devel
BuildRequires:  rust-crossbeam-utils-devel
BuildRequires:  rust-crunchy-devel
BuildRequires:  rust-csv-core-devel
BuildRequires:  rust-csv-devel
BuildRequires:  rust-diff-devel
BuildRequires:  rust-displaydoc-devel
BuildRequires:  rust-either-devel
BuildRequires:  rust-encode_unicode-devel
BuildRequires:  rust-enumflags2-devel
BuildRequires:  rust-enumflags2_derive-devel
BuildRequires:  rust-equivalent-devel
BuildRequires:  rust-errno-devel
BuildRequires:  rust-fastrand-devel
BuildRequires:  rust-getrandom0.2-devel
BuildRequires:  rust-getrandom0.3-devel
BuildRequires:  rust-gimli-devel
BuildRequires:  rust-glob-devel
BuildRequires:  rust-half-devel
BuildRequires:  rust-hashbrown-devel
BuildRequires:  rust-heck-devel
BuildRequires:  rust-heck0.4-devel
BuildRequires:  rust-http-devel
BuildRequires:  rust-httparse-devel
BuildRequires:  rust-icu_collections-devel
BuildRequires:  rust-icu_locale_core-devel
BuildRequires:  rust-icu_provider-devel
BuildRequires:  rust-is-terminal-devel
BuildRequires:  rust-itertools-devel
BuildRequires:  rust-itertools0.10-devel
BuildRequires:  rust-itertools0.13-devel
BuildRequires:  rust-itoa-devel
BuildRequires:  rust-lazy_static-devel
BuildRequires:  rust-lazycell-devel
BuildRequires:  rust-libloading-devel
BuildRequires:  rust-linux-raw-sys-devel
BuildRequires:  rust-litemap-devel
BuildRequires:  rust-log-devel
BuildRequires:  rust-matchers-devel
BuildRequires:  rust-minimal-lexical-devel
BuildRequires:  rust-miniz_oxide-devel
BuildRequires:  rust-nom7-devel
BuildRequires:  rust-num-traits-devel
BuildRequires:  rust-object-devel
BuildRequires:  rust-once_cell-devel
BuildRequires:  rust-paste-devel
BuildRequires:  rust-peeking_take_while-devel
BuildRequires:  rust-percent-encoding-devel
BuildRequires:  rust-pin-project-devel
BuildRequires:  rust-pin-project-internal-devel
BuildRequires:  rust-pin-project-lite-devel
BuildRequires:  rust-potential_utf-devel
BuildRequires:  rust-ppv-lite86-devel
BuildRequires:  rust-pretty_assertions-devel
BuildRequires:  rust-prettyplease-devel
BuildRequires:  rust-quote0.3-devel
BuildRequires:  rust-rand-devel
BuildRequires:  rust-rand_chacha-devel
BuildRequires:  rust-rand_core-devel
BuildRequires:  rust-rand_xorshift-devel
BuildRequires:  rust-rayon-core-devel
BuildRequires:  rust-rayon-devel
BuildRequires:  rust-regex-devel
BuildRequires:  rust-ring-devel
BuildRequires:  rust-rmp-devel
BuildRequires:  rust-rmp-serde-devel
BuildRequires:  rust-rustc-demangle-devel
BuildRequires:  rust-rustc-hash-devel
BuildRequires:  rust-rustc-hash1-devel
BuildRequires:  rust-rustix-devel
BuildRequires:  rust-rustversion-devel
BuildRequires:  rust-ryu-devel
BuildRequires:  rust-same-file-devel
BuildRequires:  rust-serde-devel
BuildRequires:  rust-serde_core-devel
BuildRequires:  rust-serde_derive-devel
BuildRequires:  rust-sharded-slab-devel
BuildRequires:  rust-shlex-devel
BuildRequires:  rust-simd-adler32-devel
BuildRequires:  rust-similar-devel
BuildRequires:  rust-smallvec-devel
BuildRequires:  rust-stable_deref_trait-devel
BuildRequires:  rust-strsim-devel
BuildRequires:  rust-strum0.27-devel
BuildRequires:  rust-strum_macros0.24-devel
BuildRequires:  rust-strum_macros0.27-devel
BuildRequires:  rust-subtle-devel
BuildRequires:  rust-syn1-devel
BuildRequires:  rust-synstructure-devel
BuildRequires:  rust-thread_local-devel
BuildRequires:  rust-tinystr-devel
BuildRequires:  rust-tracing-attributes-devel
BuildRequires:  rust-unarray-devel
BuildRequires:  rust-untrusted-devel
BuildRequires:  rust-utf-8-devel
BuildRequires:  rust-utf8parse-devel
BuildRequires:  rust-walkdir-devel
BuildRequires:  rust-writeable-devel
BuildRequires:  rust-yansi-devel
BuildRequires:  rust-yoke-derive-devel
BuildRequires:  rust-yoke-devel
BuildRequires:  rust-zerofrom-derive-devel
BuildRequires:  rust-zerofrom-devel
BuildRequires:  rust-zeroize-devel
BuildRequires:  rust-zerotrie-devel
BuildRequires:  rust-zerovec-derive-devel
BuildRequires:  rust-zerovec-devel

# ---------- Bundled C/C++ git-submodule dependencies ----------
Provides:       bundled(hiredis) = 1.0.2~git.bd01f10d
Provides:       bundled(libuv) = 1.48.0~git.e9f29cb9
Provides:       bundled(VectorSimilarity) = 0.8~git.d45369e0
Provides:       bundled(s2geometry) = 0.10.0~git.efb4eb8d
Provides:       bundled(RedisModulesSDK) = 0~git.8ecae317
Provides:       bundled(cpu_features) = 0.10.1
Provides:       bundled(readies)

# ---------- Bundled ScalableVectorSearch FetchContent dependencies ----------
Provides:       bundled(eve) = 2023.02.15
Provides:       bundled(robin-map) = 1.4.0
Provides:       bundled(fmt) = 11.2.0
Provides:       bundled(spdlog) = 1.15.3
Provides:       bundled(tomlplusplus) = 3.3.0

# ---------- Bundled C/C++ vendored-in-tree dependencies ----------
Provides:       bundled(snowball) = 2.1.0
Provides:       bundled(friso) = 1.6.2
Provides:       bundled(fast_float) = 7.0.0
Provides:       bundled(miniz) = 10.0.1
Provides:       bundled(nunicode)
Provides:       bundled(phonetics)
Provides:       bundled(rmutil)
Provides:       bundled(cndict)
Provides:       bundled(thpool)
Provides:       bundled(geohash)

# ---------- Bundled Rust workspace crates ----------
Provides:       bundled(crate(buffer)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(build_utils)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(c_ffi_utils)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(document)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(document_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(field)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(fnv)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(fnv_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(inverted_index)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(inverted_index_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(iterators_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(low_memory_thin_vec)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(low_memory_thin_vec_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(module_init_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(qint)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(query_error)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(query_error_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(redisearch_rs)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(result_processor)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(result_processor_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(rlookup)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(rlookup_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(rqe_iterators)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(rqe_iterators_interop)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(search_result)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(search_result_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(slots_tracker)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(slots_tracker_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(sorting_vector)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(sorting_vector_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(tracing_redismodule)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(trie_rs)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(triemap_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(types_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(value)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(value_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(varint)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(varint_ffi)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(wildcard)) = 0.0.1+git.c2ef6c041cb6
Provides:       bundled(crate(workspace_hack)) = 0.1.0

# Registry crate from ``Source1`` only (no ``rust-nix*`` %%BuildRequires; see rust block comment).
Provides:       bundled(crate(nix)) = 0.26.4

# ---------- Bundled Rust git dependencies ----------
Provides:       bundled(crate(redis-module)) = 99.99.99+git.1ab84014c096
Provides:       bundled(crate(redis-module-macros-internals)) = 99.99.99+git.1ab84014c096

Requires:       (redis >= 8.5 with redis < 8.7)
Supplements:    redis


%description
RediSearch is a Redis module that adds full-text search, secondary indexing,
vector similarity search, geographic (GEO) filtering, and aggregation
capabilities to Redis. It supports query features such as prefix matching,
fuzzy matching, phonetic matching, synonyms, and auto-complete suggestions.

This package contains the shared library (%{libname}) that can be loaded into
a Redis server with the MODULE LOAD command or via configuration.


%prep
%autosetup -p1 -a1 -n %{name}-%{upstream_version}

: Unpack FetchContent dependencies for offline builds
tar xzf %{SOURCE2}
tar xzf %{SOURCE3}
tar xzf %{SOURCE4}
tar xzf %{SOURCE5}
tar xzf %{SOURCE6}
tar xzf %{SOURCE7}

: Apply SVS compatibility patch to tomlplusplus
cd tomlplusplus-3.3.0
patch -p1 < ../deps/VectorSimilarity/deps/ScalableVectorSearch/cmake/patches/tomlplusplus_v330.patch
cd ..

: Remove macOS AppleDouble resource fork files if present
find . -name '._*' -delete

# Strip -Werror from VectorSimilarity -- Fedora: packages must not use -Werror
# GCC 16 fc44+ flags false positives in robin-map and upstream SVS code
find deps/VectorSimilarity -name CMakeLists.txt -exec sed -i 's/-Werror//g' {} +

# Note: the GPL-2.0 ``vendor/nix/test/test_kmod/hello_mod/hello.c`` fixture is
# stripped from Source0 and Source1 by makesrc.sh and makedeps.sh respectively,
# along with the matching ``.cargo-checksum.json`` entry — no in-spec mutation.

: Dummy .git marker for Rust build_utils git_root
mkdir -p .git

: Configuration file
cat << EOF | tee %{cfgname}
# RediSearch
loadmodule %{redis_modules_dir}/%{libname}
EOF

# Collect bundled-project licenses and deduplicate by content hash.
#
# The upstream tarball ships ``vendor/`` with 425+ LICENSE* files (one per
# vendored Rust crate, including dev-only crates such as criterion and
# tinytemplate that are *not* compiled into the released ``redisearch.so``).
# Naively copying every file produced ~1.5 MB of duplicate Apache-2.0 / MIT
# texts and dozens of rpmlint ``files-duplicate`` warnings.
#
# Instead, we hash each LICENSE file and keep only one canonical copy per
# unique content, named ``LICENSE-<spdx-tag>.<short-hash>``. The mapping of
# crate -> license is preserved in ``rust-vendor-licenses.txt`` (Source1) and
# installed as %%license, so per-crate provenance is not lost.
mkdir -p .licenses
cp -p deps/readies/LICENSE .licenses/LICENSE.readies 2>/dev/null || true
declare -A SEEN
for lic in vendor/*/LICENSE* vendor/*/LICENCE* vendor/*/COPYING*; do
    [ -f "$lic" ] || continue
    h=$(sha256sum "$lic" | cut -c1-12)
    if [ -z "${SEEN[$h]:-}" ]; then
        base=$(basename "$lic")
        # Strip per-crate suffix from filenames like "LICENSE-MIT-atty"
        tag=$(echo "$base" | sed -E 's/-[a-zA-Z0-9_.+-]+$//; s/^LICENSE[._-]?//; s/^LICENCE[._-]?//; s/^COPYING[._-]?//')
        [ -z "$tag" ] && tag=TEXT
        install -m 0644 "$lic" ".licenses/LICENSE-${tag}.${h}"
        SEEN[$h]=1
    fi
done


%build
# Wire up vendored Rust crate sources for offline builds.
if [ -f vendor/.cargo/config.toml ]; then
    mkdir -p .cargo
    cp -a vendor/.cargo/config.toml .cargo/config.toml
elif [ -f .cargo/config.toml ]; then
    : already in place
else
    echo "ERROR: Could not find vendor/.cargo/config.toml"
    exit 1
fi

export CARGO_HOME=$PWD/.cargo
export CARGO_NET_OFFLINE=true

: GCC 16 safety net: demote remaining -Werror diagnostics to warnings
export CXXFLAGS="${CXXFLAGS:-%{optflags}} -Wno-error=maybe-uninitialized -Wno-error=unused-but-set-variable"

%cmake \
    -DCOORD_TYPE=oss \
    -DBOOST_DIR=%{_includedir} \
    -DREDISEARCH_BUILD_SHARED=ON \
    -DBUILD_SEARCH_UNIT_TESTS=OFF \
    -DVECSIM_BUILD_TESTS=OFF \
    -DSVS_SHARED_LIB=OFF \
    -DBUILD_INTEL_SVS_OPT=0 \
    -DFETCHCONTENT_SOURCE_DIR_CPU_FEATURES=$PWD/cpu_features-0.10.1 \
    -DFETCHCONTENT_SOURCE_DIR_EVE=$PWD/eve-2023.02.15 \
    -DFETCHCONTENT_SOURCE_DIR_ROBINMAP=$PWD/robin-map-1.4.0 \
    -DFETCHCONTENT_SOURCE_DIR_FMT=$PWD/fmt-11.2.0 \
    -DFETCHCONTENT_SOURCE_DIR_SPDLOG=$PWD/spdlog-1.15.3 \
    -DFETCHCONTENT_SOURCE_DIR_TOMLPLUSPLUS=$PWD/tomlplusplus-3.3.0 \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DRUST_PROFILE=release
%cmake_build

%check
# Unit tests are disabled in CMake (``BUILD_SEARCH_UNIT_TESTS=OFF``); confirm the shared module linked.
test -x "%{__cmake_builddir}/%{libname}"

%install
install -Dpm755 %{__cmake_builddir}/%{libname} \
    %{buildroot}%{redis_modules_dir}/%{libname}
install -Dpm644 %{cfgname} \
    %{buildroot}%{redis_modules_cfg}/%{cfgname}

# Install companion shared libraries that redisearch.so links against.
find %{__cmake_builddir} \( \
    -name 'libVectorSimilarity*.so' -o \
    -name 'libcpu_features.so' \) \
    ! -type l -exec install -pm755 {} %{buildroot}%{redis_modules_dir}/ \;
for f in %{__cmake_builddir}/hiredis/libhiredis.so.* \
         %{__cmake_builddir}/hiredis/libhiredis_ssl.so.*; do
    [ -L "$f" ] || [ ! -f "$f" ] || install -pm755 "$f" %{buildroot}%{redis_modules_dir}/
done

# Install bundled fmt and spdlog shared libs (built by FetchContent).
# VectorSimilarity links against these; install them so the module is
# self-contained rather than accidentally relying on system packages.
for lib in fmt spdlog; do
    find %{__cmake_builddir}/_deps/${lib}-build -name "lib${lib}.so*" \
        ! -type l -exec install -pm755 {} %{buildroot}%{redis_modules_dir}/ \;
done
# Let ldconfig create proper soname symlinks for all companion libraries.
ldconfig -n %{buildroot}%{redis_modules_dir}

# Set RPATH to $ORIGIN only on libraries that load companion .so from
# the same directory.  Leaf libraries (hiredis, cpu_features, fmt,
# VectorSimilaritySpaces_no_optimization) must NOT be patchelf'd —
# patchelf can corrupt simple ELFs that lack complex program headers.
# libspdlog needs patchelf to replace its build-time RPATH to fmt-build.
for f in %{buildroot}%{redis_modules_dir}/redisearch.so \
         %{buildroot}%{redis_modules_dir}/libVectorSimilarity.so \
         %{buildroot}%{redis_modules_dir}/libVectorSimilaritySpaces.so; do
    [ -f "$f" ] && patchelf --set-rpath '$ORIGIN' "$f"
done
# spdlog has a build-time RPATH baked in by CMake — replace it.
for f in %{buildroot}%{redis_modules_dir}/libspdlog.so.*; do
    [ -f "$f" ] && [ ! -L "$f" ] && patchelf --set-rpath '$ORIGIN' "$f"
done


%files
# Upstream RediSearch license file (AGPL-3.0-only).
%license LICENSE.txt
# Per-crate license manifest (cargo tree --edges=normal).
%license rust-vendor-licenses.txt
# Deduplicated bundled-project license texts (one copy per unique content).
%license .licenses/*
%doc *.md
# search.conf is a plain "loadmodule ..." stub with no secrets; default
# 0644 root:root keeps rpmlint happy and matches Fedora policy for
# %%config files. The redis package owns /etc/redis and the modules dir.
%dir %{redis_modules_cfg}
%config(noreplace) %{redis_modules_cfg}/%{cfgname}
%dir %{redis_modules_dir}
%{redis_modules_dir}/%{libname}
%{redis_modules_dir}/lib*.so*


%changelog
* Sun Apr 26 2026 Angel Yanev <angel.yanev@redis.com> - 1.0.0-1
- Initial development packaging.
