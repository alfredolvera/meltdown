# Decision log

## D-001 — Initial revision: v1.5d

**Status:** accepted, 2026-09-03.

Use the `kinst` set with BIOS `v1.5d` as the primary reference. All nine ZIP
members and the combined CHD SHA-1 match the MAME manifest. Addresses from
different game revisions must never be mixed.

## D-002 — PC before Nintendo 64

**Status:** accepted, 2026-09-03.

Linux provides fast instrumentation, sanitizers, and differential tests. The
core is kept platform-independent from the beginning, but libdragon is not on
the proof-of-concept critical path.

## D-003 — Traces are observable truth

**Status:** accepted, 2026-09-03.

Ghidra helps form hypotheses; MAME provides the observable state used to test
them. Readable pseudocode without dynamic evidence remains `unverified`.

## D-004 — Game data stays outside the repository

**Status:** accepted, 2026-09-03.

The repository stores fingerprints, metadata, tools, and original
reconstruction work. It does not store ROMs, CHDs, memory dumps, or substantial
asset exports.

## D-005 — Per-function provenance

**Status:** accepted, 2026-09-03.

Every recovered function has an independent JSON record linking the game
revision, address, assembly, reconstruction, and verification evidence. A
function is not accepted without this record.

## D-006 — Isolate AGPL references

**Status:** accepted, 2026-09-03.

The external `nekuz0r/ki-rom` repository stays under the ignored `work/`
directory. Its tools may be executed and factual results verified against our
dumps, but AGPL source is not copied into Meltdown without an explicit decision
about the project's license.

## D-007 — Ghidra uses 32-bit addresses

**Status:** accepted, 2026-09-03.

Import KI as `MIPS:LE:64:64-32addr` with the `n32` compiler specification. The
R4600 has 64-bit registers while the observed software uses a 32-bit virtual
address space. Ghidra 12.1.3 declares this exact combination.

## D-008 — Native recompilation, not matching decompilation

**Status:** accepted, 2026-09-03.

Meltdown aims to run authentic KI logic natively on PC. It does not seek a
byte-identical ROM, the original compiler, or source that reproduces the
original assembly. Verified decompilation is useful where it improves clarity;
static recompilation is equally valid where it preserves behavior more directly.
