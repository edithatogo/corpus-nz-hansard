# Package And CLI Migration Execution

Release status: release-ready-package-cli-compatibility-layer.

The package/CLI migration has been executed as a compatibility layer. The repository now has `src/nz_hansard_corpus`, a package-backed `nzhc` CLI, and legacy console names routed through `nz_hansard_corpus.cli:main`.

The command surface includes `nzhc build-manifest`, `nzhc validate`, `nzhc metadata build`, `nzhc hf stage`, and `nzhc zenodo draft`.

The legacy scripts remain supported and the publication boundary is preserved.
