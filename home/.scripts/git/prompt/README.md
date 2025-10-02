# git-prompt

Fast git prompt written in Rust using libgit2.

## Compilation

```bash
cargo build --release
```

The binary will be at `target/release/git-prompt`.

## Installation

Copy the binary to the desired location:

```bash
cp target/release/git-prompt git-prompt
```

## Output Format

The prompt shows:
- Depth in repository (`.` per directory level)
- Branch name (or short commit hash if detached HEAD)
- `+` if working tree is dirty (modified/staged/untracked files)
- `&` if there are stashed changes

Example: ` ...master+&` means:
- Three directories deep in repo
- On branch `master`
- Working tree has changes
- Has stashed changes
