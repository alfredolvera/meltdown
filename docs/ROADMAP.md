# Proof of concept: 50–100 hours

These are ranges of effective work, not calendar estimates. Every phase has a
verifiable deliverable before the scope expands.

| Phase | Cumulative hours | Deliverable |
|---|---:|---|
| 0. Identity and environment | 0–8 | Exact revision, fingerprints, reproducible MAME setup |
| 1. Boot and memory maps | 8–20 | Boot traces, RAM/ROM/IDE maps, and snapshots |
| 2. Ghidra project | 20–35 | Correct architecture and blocks, initial symbols |
| 3. Main flow | 35–55 | Documented boot → load → main-loop chain |
| 4. Candidate routine | 55–75 | Bounded function, known I/O, stable assembly |
| 5. Native execution | 75–90 | Original routine running outside MAME on PC |
| 6. Differential comparison | 90–100 | Reproducible cases and complete provenance |

## Gate 0: identify the inputs

KI v1.5d is the fixed initial target. Its boot ROM, eight audio ROMs, and CHD
have been identified against MAME, and the CHD passed full `chdman` verification.
Addresses from other revisions must never be mixed into this analysis.

Required evidence:

- pinned MAME version;
- boot-ROM SHA-1 and CRC;
- verified logical CHD SHA-1;
- exact command that starts the game; and
- snapshots surrounding the boot and loaded runtime state.

## First native candidate

The first candidate is selected for clean boundaries, not visual impact. A good
routine should be:

- called often and easy to stop in MAME;
- bounded, with few hardware dependencies;
- driven by small inputs that can be captured;
- observable through registers or compact memory regions; and
- free of self-modifying code for the first experiment.

A checksum, conversion, table, math, or bounded animation routine may be a
better first target than the whole main loop. The proof of concept demonstrates
the extraction, translation, and comparison method; it does not need to display
a fight yet.

## Success criterion

The proof of concept is complete when one authentic routine from KI v1.5d:

1. has documented addresses, bytes, assembly, and call sites;
2. executes natively on Linux;
3. consumes fixtures captured from the emulated arcade system;
4. matches registers, memory, and return values across multiple cases; and
5. has a provenance record accepted by the automatic validator.
