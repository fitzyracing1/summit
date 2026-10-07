# scanrepo

Physical copy of a git repo. Print it. Read it. Scan it back.

Kind: `scanrepo`  
Extension: `.scanrepo`  
MIME: `application/x-scanrepo`  
Version: 1

Files:

- `scanrepo.kind` — format declaration
- `sample.scanrepo` — digital master of a two-file repo
- `scanrepo-restore.py` — checks blob hashes and rebuilds a git repo from the master

The printable PDF is generated from `sample.scanrepo` (cover plus one page per file). It is not in this commit because the push path is text-only.

## What a booklet is

One edition is one commit. The cover carries repo name, edition, branch, commit id, tree id, and parent. Each later page is one file (or one chunk of a file) in monospace, plus a QR code that holds the same bytes.

A new printing does not overwrite the old one. Bump edition, set `parent` to the previous commit, print again. The shelf is the history.

## Scan path

1. Photograph every page, cover included. Do not crop the codes.
2. Decode each QR. Cover payload starts with `C|`. Page payload starts with `P|`.
3. Rejoin chunks, check each blob with git's `blob <len>\0` SHA-1.
4. Rebuild the tree (names sorted, git style) and the commit. Reject the booklet if either id does not match the cover.

Phone QR apps are enough for this sample. Bigger files need chunked codes (about 1800 source characters per page).

## Limits

This is a snapshot format, not a packfile. Deltas and binary assets are out. A 50 KB text repo is a thin booklet. A photo-heavy repo is the wrong thing to print.
