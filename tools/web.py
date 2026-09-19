#!/usr/bin/env python3
"""tools/web.py - the estate's actual mesh, measured.

A GRID IS THE MESH YOU DO NOT HAVE TO STORE. Its connectivity is implicit in the index: neighbours
are found by arithmetic. A general mesh has to carry its connectivity, because nothing generated
it from a rule.

The real universe is the second kind. Its large scale structure is the cosmic web, and it grew
from a Gaussian random field of primordial density fluctuations, so no rule produces it and no
index gives its filaments. Connectivity there is history, not law, and history has to be measured.

The estate is the same. Its repositories are not adjacent because a law put them next to each
other; they are adjacent when they actually SHARE CONTENT. Git already decides this and cannot be
argued with: a blob SHA is the hash of the content, so two repositories holding the same SHA hold
byte identical content. That is an exact adjacency with a cryptographic key behind it.

    edge(A, B)  =  the blobs whose SHA appears in both A and B

This measures every blob in every repository's history, intersects them, and writes the graph.
Nothing is inferred, nothing is weighted by guesswork, and a pair with nothing in common gets no
edge at all, which is how the voids appear.

Writes:
  web/nodes.tsv   repo  blobs  bytes  degree  shared_blobs  class
  web/edges.tsv   a  b  shared_blobs  shared_bytes
  web-meta.json   the totals and the checks

Repositories that are not confirmed public are given one of our own words and a number. The counts
are the point; the name is somebody else's business.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from itertools import combinations


def git_blobs(d):
    """Every blob in every reachable and unreachable object of this repository, with its size."""
    p = subprocess.run(['git', 'cat-file', '--batch-all-objects',
                        '--batch-check=%(objectname) %(objecttype) %(objectsize)'],
                       cwd=d, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = {}
    for line in p.stdout.splitlines():
        f = line.split()
        if len(f) == 3 and f[1] == 'blob':
            out[f[0]] = int(f[2])
    return out


def public_set(org):
    try:
        r = subprocess.run(['gh', 'repo', 'list', org, '--limit', '300',
                            '--json', 'name,visibility', '--jq',
                            '.[] | select(.visibility=="PUBLIC") | .name'],
                           capture_output=True, text=True)
        s = {n.strip().lower() for n in r.stdout.split() if n.strip()}
        return s or None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--roots', default='C:/Users/vikra/Documents/GitHub')
    ap.add_argument('--org', default='Ventusltd')
    ap.add_argument('--out', default='.')
    a = ap.parse_args()

    repos = []
    for root in a.roots.split(','):
        if not os.path.isdir(root):
            continue
        for n in sorted(os.listdir(root)):
            d = os.path.join(root, n)
            if os.path.isdir(os.path.join(d, '.git')):
                repos.append((n, d))
    if not repos:
        print('FAIL: zero repositories. A check that examines nothing refuses.')
        return 1

    t0 = time.time()
    names = [n for n, _ in repos]
    blobs = []
    size = {}
    for i, (n, d) in enumerate(repos):
        b = git_blobs(d)
        size.update(b)
        blobs.append(set(b))
        print('  %-36s %8s blobs %6.1f s' % (n, format(len(b), ','), time.time() - t0),
              file=sys.stderr, flush=True)

    # where each blob lives. A blob in one repository only is that repository's own; a blob in
    # several is an edge, and the more repositories it is in the more of a knot it makes.
    where = {}
    for i, s in enumerate(blobs):
        for sha in s:
            where.setdefault(sha, []).append(i)

    edge = {}
    for sha, rs in where.items():
        if len(rs) < 2:
            continue
        for x, y in combinations(sorted(rs), 2):
            e = edge.setdefault((x, y), [0, 0])
            e[0] += 1
            e[1] += size.get(sha, 0)

    deg = [0] * len(repos)
    shared = [0] * len(repos)
    for (x, y), (nb, by) in edge.items():
        deg[x] += 1
        deg[y] += 1
        shared[x] += nb
        shared[y] += nb

    # THE CLASSIFICATION IS BY DEGREE, AND IT IS AN ANALOGUE, NOT THE REAL THING. Cosmology
    # classifies the web by counting how many eigenvalues of the deformation tensor exceed a
    # threshold, which needs a continuous density field. A graph has no such field, so this counts
    # neighbours instead and says so, rather than borrowing a method it is not entitled to.
    def klass(k):
        if k == 0: return 'void'         # shares nothing with anything: an island
        if k == 1: return 'leaf'
        if k == 2: return 'filament'
        return 'knot'

    pub = public_set(a.org)
    label = list(names)
    redacted = 0
    if pub:
        k = 0
        for i, n in enumerate(names):
            if n.lower() not in pub:
                k += 1
                label[i] = 'unnamed-%02d' % k
        redacted = k
    else:
        print('  WARNING: could not confirm which repositories are public. Names left as they '
              'are; do not publish this without checking.', file=sys.stderr)

    os.makedirs(os.path.join(a.out, 'web'), exist_ok=True)
    with open(os.path.join(a.out, 'web', 'nodes.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# repo\tblobs\tbytes\tdegree\tshared_blobs\tclass\n')
        for i, n in enumerate(label):
            by = sum(size.get(s, 0) for s in blobs[i])
            f.write('%s\t%d\t%d\t%d\t%d\t%s\n'
                    % (n, len(blobs[i]), by, deg[i], shared[i], klass(deg[i])))

    with open(os.path.join(a.out, 'web', 'edges.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# a\tb\tshared_blobs\tshared_bytes\n')
        for (x, y), (nb, by) in sorted(edge.items(), key=lambda kv: -kv[1][0]):
            f.write('%s\t%s\t%d\t%d\n' % (label[x], label[y], nb, by))

    distinct = len(where)
    n = len(repos)
    meta = {
        'asof': datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'),
        'command': 'python tools/web.py ' + ' '.join(sys.argv[1:]),
        'repositories': n,
        'distinct_blobs': distinct,
        'blobs_in_one_repository_only': sum(1 for v in where.values() if len(v) == 1),
        'blobs_shared': sum(1 for v in where.values() if len(v) > 1),
        'edges': len(edge),
        'possible_edges': n * (n - 1) // 2,
        'density': round(len(edge) / max(1, n * (n - 1) // 2), 4),
        'voids': sum(1 for d_ in deg if d_ == 0),
        'leaves': sum(1 for d_ in deg if d_ == 1),
        'filaments': sum(1 for d_ in deg if d_ == 2),
        'knots': sum(1 for d_ in deg if d_ >= 3),
        'largest_degree': max(deg) if deg else 0,
        'redacted_repositories': redacted,
        'seconds': round(time.time() - t0, 1),
        'method': 'a blob SHA is the hash of its content, so a SHA present in two repositories '
                  'means byte identical content in both. The adjacency cannot be wrong.',
        'not_measured': 'imports, forks, references and citations are also real edges and none of '
                        'them are here. This graph is shared content and nothing else.'
    }
    with open(os.path.join(a.out, 'web-meta.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(meta, f, indent=1, sort_keys=True)
    print(json.dumps(meta, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
