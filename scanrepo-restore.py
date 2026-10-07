#!/usr/bin/env python3
"""Restore a scanrepo master into a git repo and verify printed ids."""
import hashlib
import subprocess
import sys
from pathlib import Path


def git_blob(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def git_tree(entries):
    body = b""
    for mode, name, sha in sorted(entries, key=lambda e: e[1]):
        body += f"{mode} {name}\0".encode() + bytes.fromhex(sha)
    header = f"tree {len(body)}\0".encode()
    return hashlib.sha1(header + body).hexdigest()


def parse(text: str):
    lines = text.splitlines()
    if not lines or lines[0] != "# scanrepo v1":
        raise SystemExit("not a scanrepo v1 file")
    if lines[1] != "---":
        raise SystemExit("missing frontmatter")
    meta = {}
    i = 2
    while lines[i] != "---":
        k, v = lines[i].split(": ", 1)
        meta[k] = v
        i += 1
    i += 1
    pages = []
    while i < len(lines):
        if lines[i].startswith("## PAGE "):
            i += 1
            header = {}
            while lines[i] != "text:":
                k, v = lines[i].split(": ", 1)
                header[k] = v
                i += 1
            i += 1
            body = []
            while lines[i] != "## END PAGE":
                body.append(lines[i])
                i += 1
            header["bytes"] = ("\n".join(body) + "\n").encode()
            pages.append(header)
        i += 1
    return meta, pages


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "sample.scanrepo")
    dest = Path(sys.argv[2] if len(sys.argv) > 2 else "paper-git-restored")
    meta, pages = parse(src.read_text())
    by_path = {}
    for page in pages:
        by_path.setdefault(page["path"], []).append(page)
    entries = []
    dest.mkdir(parents=True, exist_ok=True)
    for path, chunks in by_path.items():
        chunks.sort(key=lambda p: int(p["chunk"]))
        data = b"".join(p["bytes"] for p in chunks)
        blob = git_blob(data)
        if blob != chunks[0]["blob"]:
            data = data[:-1] if data.endswith(b"\n") else data
            blob = git_blob(data)
        if blob != chunks[0]["blob"]:
            raise SystemExit(f"blob mismatch for {path}: got {blob} want {chunks[0]['blob']}")
        out = dest / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        entries.append((chunks[0]["mode"], path, blob))
        print(f"ok  {path}  {blob[:12]}")
    tree = git_tree(entries)
    if tree != meta["tree"]:
        raise SystemExit(f"tree mismatch: got {tree} want {meta['tree']}")
    print(f"ok  tree {tree}")
    print(f"cover commit {meta['commit']}  (parent {meta['parent']})")
    subprocess.run(["git", "init", "-q"], cwd=dest, check=True)
    subprocess.run(["git", "add", "."], cwd=dest, check=True)
    print(f"restored files in {dest}")


if __name__ == "__main__":
    main()
