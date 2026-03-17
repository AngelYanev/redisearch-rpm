Name:           redisearch
Version:        8.6.0
Release:        1%{?dist}
Summary:        Full-text search, vector similarity, and secondary indexing module for Redis

License:        (RSALv2 OR SSPLv1 OR AGPL-3.0-only) AND MIT AND Apache-2.0 AND BSD-3-Clause
URL:            https://github.com/RediSearch/RediSearch

# Source tarball must include git submodule contents (hiredis, libuv,
# VectorSimilarity, RedisModulesSDK, s2geometry, etc.)
Source0:        https://github.com/AngelYanev/redisearch-rpm/releases/download/v%{version}/redisearch-%{version}.tar.gz
# Vendored Rust crates (generated with: cd src/redisearch_rs && cargo vendor ../../vendor)
Source1:        https://github.com/AngelYanev/redisearch-rpm/releases/download/v%{version}/redisearch-vendor-%{version}.tar.gz

%global redis_modules_dir %{_libdir}/redis/modules
%global redis_confdir     %{_sysconfdir}/redis/modules
%global libname redisearch.so
%global cfgname redisearch.conf

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cmake >= 3.13
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  openssl-devel
BuildRequires:  rust >= 1.91
BuildRequires:  cargo
BuildRequires:  rust-packaging
BuildRequires:  cargo-rpm-macros
BuildRequires:  boost-devel >= 1.83
BuildRequires:  redis-devel
BuildRequires:  clang-devel

# ---------- Bundled C/C++ git-submodule dependencies ----------
Provides:       bundled(hiredis) = 1.0.2~git.bd01f10d
Provides:       bundled(libuv) = 1.48.0~git.e9f29cb9
Provides:       bundled(VectorSimilarity) = 0.8~git.d45369e0
Provides:       bundled(s2geometry) = 0.10.0~git.efb4eb8d
Provides:       bundled(RedisModulesSDK) = 0~git.8ecae317

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

# ---------- Bundled Rust git dependencies ----------
Provides:       bundled(crate(redis-module)) = 99.99.99+git.1ab84014c096
Provides:       bundled(crate(redis-module-macros-internals)) = 99.99.99+git.1ab84014c096

Supplements:    redis

%description
RediSearch is a Redis module that adds full-text search, secondary indexing,
vector similarity search, geo filtering, and aggregation capabilities to Redis.
It supports query features such as prefix matching, fuzzy matching, phonetic
matching, synonyms, and auto-complete suggestions.

This package contains the shared library (%{libname}) that can be loaded into
a Redis server with the MODULE LOAD command or via configuration.

%prep
%autosetup -n redisearch-%{version} -a 1

cat > %{cfgname} <<'EOF'
loadmodule %{redis_modules_dir}/%{libname}
EOF

%build
# Wire up the vendored Rust crate sources so cargo works offline.
# The vendor tarball ships vendor/.cargo/config.toml with the correct
# [source] replacement entries (including the redismodule-rs git dep).
# Cargo finds .cargo/config.toml by searching parent directories, so
# placing it at the project root covers src/redisearch_rs/ invocations.
%cargo_prep -v vendor
if [ -f vendor/.cargo/config.toml ]; then
  mkdir -p .cargo
  cp -a vendor/.cargo/config.toml .cargo/config.toml
else
  echo "ERROR: Could not find vendor/.cargo/config.toml"
  exit 1
fi
%cargo_vendor_manifest vendor

export CARGO_HOME=$PWD/.cargo
export CARGO_NET_OFFLINE=true

%cmake \
  -DCOORD_TYPE=oss \
  -DBOOST_DIR=%{_includedir} \
  -DREDISEARCH_BUILD_SHARED=ON \
  -DBUILD_SEARCH_UNIT_TESTS=OFF \
  -DRUST_PROFILE=release
%cmake_build

%install
install -Dpm755 %{__cmake_builddir}/%{libname} \
  %{buildroot}%{redis_modules_dir}/%{libname}
install -Dpm644 %{cfgname} \
  %{buildroot}%{redis_confdir}/%{cfgname}

%files
%license LICENSE.txt
%license licenses/
%license cargo-vendor.txt
%doc README.md CONTRIBUTING.md
%{redis_modules_dir}/%{libname}
%config(noreplace) %{redis_confdir}/%{cfgname}

%changelog
* Mon Mar 17 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-1
- Initial package for RediSearch module
