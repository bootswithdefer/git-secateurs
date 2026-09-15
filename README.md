[![CI](https://github.com/bootswithdefer/git-secateurs/workflows/CI/badge.svg?event=push)](https://github.com/bootswithdefer/git-secateurs/actions?query=workflow%3ACI) [![crates.io](https://img.shields.io/crates/v/git-secateurs.svg)](https://crates.io/crates/git-secateurs)

git-secateurs
=============

<img src="images/logo.svg" alt="git-secateurs logo" width="1000">


`git-secateurs` automatically trims local tracking branches whose upstream branches are merged or stray.

It is the missing companion to `git fetch --prune`: a safer, faster alternative to hand-rolled branch-deletion one-liners. It inspects whether an upstream is *fully merged* into the base (not merely gone), so it will not silently delete unmerged work.

## Installation

Install with cargo:

```shell
cargo install git-secateurs
```

Or download a binary from [Releases](https://github.com/bootswithdefer/git-secateurs/releases) and place it on your `PATH`.

`git-secateurs` uses [`git2`](https://crates.io/crates/git2), which links against `openssl` on \*nix. Building from source may require `libssl-dev` and `pkg-config`.

## Usage

1. Set an upstream for branches you want trimmed (`git push -u <remote> <branch>` does this on push).
2. Run `git secat`. It recognizes merged or stray branches and deletes them.
3. Use `git secat --dry-run` to preview without deleting.

For git-flow, set your base branches:

```shell
git config secat.bases develop,master
```

## Configuration

Configured via git config under the `secat.*` namespace (`secat.bases`, `secat.protected`, `secat.confirm`, `secat.update`, …). See `git secat --help` or the [man page](docs/git-secat.1) for the full list.

## How it works

`git-secateurs` classifies each tracking branch and only deletes it when it is safe:

- **merged** — the upstream is fully merged into the upstream of a base branch, so no changes are lost.
- **stray** — the upstream is gone but the branch is *not* proven merged (e.g. a rejected PR, or an amended/rebased branch). These are surfaced separately because deleting them may lose work.

It is merge-style agnostic and detects:

- merge commits (`git merge --no-ff`)
- rebase / fast-forward merges (`git cherry` equivalence)
- squash merges

It supports GitHub flow, git flow, and simple/triangular remote workflows, can `push --delete` remote branches you forgot to remove, and runs classification in parallel for large repositories.

## Disclaimers

Git and the Git logo are either registered trademarks or trademarks of Software Freedom Conservancy, Inc., corporate home of the Git Project, in the United States and/or other countries.

The `git-secateurs` logo is not derived from or affiliated with the Git project. The secateurs illustration is by [Klàro](https://openclipart.org/artist/Kl%C3%A0ro) via [Openclipart](https://openclipart.org/detail/246324/snoeischaar), released into the public domain (CC0).
