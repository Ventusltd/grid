# grid

**What is a grid?**

A grid is the mesh you do not have to store.

That is the whole definition, and everything below is its consequences.

## The words, used exactly

These get used interchangeably and they are not the same thing.

| word | what it is | connectivity |
|---|---|---|
| **lattice** | a set of points with translational symmetry, repeating forever | implied by the basis vectors |
| **grid** | a partition of a domain at fixed pitch, indexed by (i, j) | **computed** from the index |
| **mesh** | a partition of a domain into cells | **stored**, explicitly |
| **graph** | nodes and edges, no geometry required | stored |
| **web** | a graph with knots, filaments, walls and voids | stored, and measured |

So: **every grid is a mesh. Almost no mesh is a grid.** A grid is the special case where
neighbours are found by arithmetic on the index, so the connectivity never has to be carried. An
unstructured mesh must carry it, because nothing generated it from a rule.

That distinction is not pedantry. It decides whether a thing can be drawn from a single integer or
has to be loaded.

## The actual universe is a mesh, not a grid

Its large scale structure is the **cosmic web**: knots, filaments, walls, voids. This is measured,
by redshift survey (CfA, 2dF, SDSS, DESI) and reproduced by N-body simulation.

The formal classification counts eigenvalues of the deformation tensor above a threshold: none
gives a **void**, one a **wall**, two a **filament**, three a **knot**.

The mechanism is Zel'dovich (1970). Gravitational collapse is anisotropic: matter falls together
first along one axis into a sheet, then a second into a filament, then a third into a cluster. A
web is what that necessarily makes. A lattice is what it cannot make.

What is measured about it:

- voids hold roughly **80% of the volume** and a small share of the mass, with diameters of 30 to
  100 Mpc
- **Laniakea**, our supercluster, about 520 million light years across, and defined by velocity
  flow, which is to say by connectivity rather than by a boundary
- statistical homogeneity only appears **above about 100 Mpc/h**, roughly 300 million light years.
  Below that the universe is not homogeneous. It is the web.

And the reason it can never be a grid: the web grew from **primordial density fluctuations**, a
nearly scale invariant Gaussian random field (n_s about 0.965) imprinted in the CMB at
one part in 100,000. A random field has no generating rule. You cannot compute where a filament
is from an index, at any resolution, ever.

**The structure is contingent. It is history, not law.**

## The division this forces

| structure comes from | positions and edges are | must be |
|---|---|---|
| **a rule**: stepper pitch, crystal lattice, a golden angle spiral | computed from the index | never stored |
| **history**: the cosmic web, a power network, who shares content with whom | measured | stored, with explicit connectivity |

Confusing the two is the most expensive error available here. Drawing historical structure with a
rule produces a picture that is tidy, fast, and a lie. Storing rule generated structure wastes
memory that the rule was going to give you for nothing.

## What mathematics allows

Grids are not a free choice. They are heavily constrained, and the constraints are theorems.

- **Exactly three regular tessellations of the plane**: triangle, square, hexagon.
- **Exactly five** two dimensional Bravais lattices; **fourteen** in three dimensions.
- **Crystallographic restriction**: a lattice admits only 2, 3, 4 and 6 fold rotation.
  **Five fold symmetry is impossible in a lattice.** Quasicrystals (Shechtman, 1982) are
  aperiodic precisely because they show it.
- **Densest circle packing in the plane is hexagonal**, density pi/sqrt(12), about 0.9069
  (Thue; rigorously Fejes Toth). In three dimensions, pi/sqrt(18), about 0.7405: Kepler's
  conjecture, proved by Hales.
- **Honeycomb theorem** (Hales, 1999): the hexagonal grid is the least perimeter partition of the
  plane into equal areas.

And the result that decides which law any drawing may use:

> **You cannot have both a lattice and isotropy.**

A grid always has preferred axes, capped at six fold. The golden angle has no preferred axis
because the golden ratio is the hardest number to approximate by rationals, so it never resonates
into lattice lines. Therefore the placement law is not a matter of taste. It is fixed by whether
the object has a preferred axis:

- a wafer does, the scanner's x and y, so it gets a **grid**
- a cluster of galaxies does not, so it gets the **golden angle**
- a network has no geometry of its own at all, so it gets a **graph** and its coordinates come
  from somewhere else, usually the ground

## Where this lands in cables and grids

The theory is not decorative here. It is already in the standards.

**IEC 60228 stranding.** Class 2 conductors come in 7, 19, 37, 61, 91 wires. Those are the
**centred hexagonal numbers**, 3n^2 + 3n + 1: one wire, then a ring of 6, then 12, then 18.
Stranded cable is the densest two dimensional circle packing, found by ropemakers centuries before
it was proved. Compaction then deforms those circles to push fill factor from about 0.75 toward
0.90 and above, buying what packing theory says round wires cannot reach, and smoothing the field
concentrators while it does it.

**Trefoil is the unit cell of that same packing**: three touching circles, the densest and most
symmetric arrangement three conductors can take. It is rewarded for the reason the honeycomb is.

**The electrical grid is not a grid.** The word is historical, from the gridiron layout of early
distribution. Topologically it is an unstructured graph, near planar but not a lattice, and its
connectivity must be stored. Giving a power network the grid law would be a false statement about
the network.

## The estate, measured as a mesh

Prose about webs is worth nothing without an edge set, so here is one, and it is exact.

Git already decides adjacency and cannot be argued with. A blob SHA is the hash of its content, so
the same SHA in two repositories means **byte identical content in both**. That is an adjacency
with a cryptographic key behind it.

    edge(A, B) = the blobs whose SHA appears in both A and B

Measured 2026-09-19 by `tools/web.py`, in 3.4 seconds:

| quantity | value |
|---|---|
| repositories | 68 |
| distinct blobs | 42,813 |
| blobs in one repository only | 40,578 |
| blobs shared by two or more | 2,235 |
| edges | 602 of 2,278 possible |
| density | 0.2643 |
| **voids** (share nothing with anything) | **13** |
| leaves (one neighbour) | 5 |
| filaments (two neighbours) | 2 |
| knots (three or more) | 48 |
| largest degree | 39 |

The strongest filaments:

| a | b | shared blobs | shared bytes |
|---|---|---|---|
| globalgrid2050 | testcode | 1,246 | 153,469,137 |
| globalgrid2050 | pipelinenews | 546 | 80,994,294 |
| galaxies-wafers | testcode | 267 | 4,916,942 |
| pipelinenews | testcode | 142 | 19,309,258 |

Two things fell out of this that a list of repositories cannot show.

**A misspelling is visible as structure.** `globalgrid2050-homepage` and `globalgrid2050-hompage`
share 57 blobs. Two repositories exist where one was meant, and the mesh found it without being
asked, because shared content is the only evidence needed.

**The count moved while it was being measured.** The estate was 67 repositories an hour earlier
and is 68 here, because creating this repository added a node. A measured system includes the act
of measuring it, and the honest response is to timestamp the number rather than to round it.

## The laws, each with a way to be shown wrong

**L1. A grid's connectivity is computed; a mesh's is stored.**
Falsified by any grid here whose neighbours cannot be derived from its index.

**L2. Rule generated structure is never stored; historical structure is never invented.**
Falsified by any position in a drawing that came from neither a stated rule nor a measurement.

**L3. An edge must carry a key.**
Every adjacency in `web/edges.tsv` is a set of blob SHAs present in both repositories. Falsified
by any edge that cannot be reproduced by `git cat-file --batch-all-objects` on both ends.

**L4. A void is a measured absence, not an unmeasured one.**
The 13 voids share no content with anything, and that was checked against all 67 others.
Falsified by any void that was simply never compared.

**L5. The placement law is fixed by the object, not chosen.**
A thing with a preferred axis gets a grid; a thing without one gets the golden angle; a network
gets a graph. Falsified by any drawing whose law contradicts the object's symmetry.

**L6. A name is disclosure.**
Repositories not confirmed public are given one of our own words and a number. The counts are the
point; the name is somebody else's business. Falsified by any private name appearing here.

## What is not measured

This graph is **shared content and nothing else**. Imports, forks, references, citations,
dependencies and people are all real edges, and none of them are in here. The web is therefore a
lower bound on the estate's connectivity, never an upper one.

The degree classification is **an analogue and is labelled as one**. Cosmology classifies the web
by eigenvalues of a deformation tensor, which needs a continuous density field. A graph has no
such field, so this counts neighbours instead rather than borrowing a method it is not entitled
to.

Nothing here is simulated. Where a number is computed rather than measured it says so.

## Licence

Open to all. The code is under the Apache License 2.0 (see LICENSE). Original text, tables and ledgers produced by this repository are under CC BY 4.0: use them, and say where they came from. Material belonging to others keeps its own licence, named beside it; standards are cited by clause and value and never reproduced.
