# Patches

Both patches fix upstream issues when building RediSearch against Fedora's
system libraries. They should be upstreamed — once merged, drop the `.patch`
files and their `Patch:` lines from the spec.

## redisearch-svs-header-guard.patch

VectorSimilarity's `tiered_factory.h` unconditionally includes
`VecSim/algorithms/svs/svs_tiered.h`, but Intel's SVS (Scalable Vector Search)
library isn't packaged for Fedora so we build with `-DUSE_SVS=OFF`.  The header
doesn't exist, and compilation fails.

The patch wraps the include in `#if HAVE_SVS` so it's only pulled in when SVS
is actually enabled.

**File:** `deps/VectorSimilarity/src/VecSim/index_factories/tiered_factory.h`

**Alternatives considered:**
- Create a dummy empty `svs_tiered.h` stub — works but feels hackier than
  guarding the include properly.

## redisearch-boost-sha1-compat.patch

Fedora 43 ships Boost 1.87.  Starting with Boost 1.86,
`boost::uuids::detail::sha1::get_digest()` changed its signature from
`unsigned char*` to `unsigned int (&)[5]` (`digest_type`).  RediSearch still
calls the old form, so compilation fails.

The patch updates `Sha1_Compute()` to use the new `digest_type` API and
manually unpacks the digest words into the existing byte array.

**File:** `src/util/hash/hash.cpp`

**Alternatives:** None — the code must be updated for the newer Boost API.
