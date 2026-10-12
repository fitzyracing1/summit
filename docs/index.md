# summit (scanrepo format origin)

This repo is where the **scanrepo** format started: a physical copy of a git repo that you print, read, and scan back. Its README is titled "scanrepo". The maintained tools and GitHub Action now live in [scanrepo-action](https://github.com/fitzyracing1/scanrepo-action).

- Kind `scanrepo`, extension `.scanrepo`, MIME `application/x-scanrepo`, version 1

| File | Content |
|---|---|
| `scanrepo.kind` | format declaration: structure, parse rules, write rules |
| `sample.scanrepo` | digital master of a two-file repo |
| `scanrepo-restore.py` | checks blob hashes and rebuilds a git repo from the master |
| `docs/index.html` | GitHub Pages site (deployed by `.github/workflows/pages.yml`) |

## Getting started

```sh
python3 scanrepo-restore.py sample.scanrepo paper-git-restored
```

Both arguments are optional. The defaults are `sample.scanrepo` and `paper-git-restored`.

## Format summary (from `scanrepo.kind`)

Line 1 is `# scanrepo v1`. YAML frontmatter holds `repo, edition, branch, commit, tree, parent, pages`, and `parent` may be `none`. Page blocks run from `## PAGE <n>` to `## END PAGE`. Each one has `path, mode, blob, chunk, chunk_of` header lines, then `text:`, then the file bytes. Pages must be numbered 1..pages with no gaps.

One edition is one commit. A new printing bumps the edition and sets `parent`. This is a snapshot format, so deltas and binary assets are not supported.

This repo has no LICENSE file.

Copyright (c) 2026 Joshua Almeida
