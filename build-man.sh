#!/usr/bin/env bash

MODE=$1
case $MODE in
build)
    cargo build --bin build-man --features build-man
    ;;
run|"")
    mkdir -p docs/
    # Only generate the deterministic roff source. A `man`-rendered plain-text
    # copy was intentionally dropped: its output depends on the local man/groff
    # implementation (GNU vs BSD), which made `docs-are-up-to-date` non-portable.
    cargo run --bin build-man --features build-man > docs/git-secat.1
    ;;
*)
    echo "Unknown mode: $MODE"
    exit -1
    ;;
esac
