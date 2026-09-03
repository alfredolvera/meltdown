# Project charter

## Intended outcome

A faithful native PC port of the 1994 Killer Instinct arcade game, created as a
research and learning project. Nintendo 64 work begins only after the PC core is
testable and sufficiently independent of its host platform.

## Project classification

Meltdown is a native recompilation and reverse-engineering project. Decompilation
is a supporting method, not the final product.

The project does **not** require:

- source code identical to Rare's original source;
- the original compiler or build environment;
- a byte-identical reconstruction of the U98 ROM;
- matching assembly for newly compiled code.

Success means that authentic game logic runs natively and reproduces the
observable and internal behavior that matters to gameplay.

## What counts as original game logic

- C/C++ reconstructed from an identified and documented MIPS routine.
- Static translation of original MIPS instructions with verified semantics.
- Data derived at runtime from the user's lawfully obtained dumps.

An implementation written only to imitate what appears on screen does not count
as recovered game logic. A temporary implementation of that kind must be marked
as a `placeholder` and cannot be considered complete.

## Permitted new code

- Input, video, audio, files, timing, and other platform interfaces.
- Extraction, analysis, tracing, translation, and comparison tools.
- Native execution harnesses and tests.
- Explicit adapters replacing arcade-board registers and devices.

Every boundary between recovered logic and a hardware replacement must remain
visible in both the source and the provenance record.

## Data policy

- The repository never stores ROMs, CHDs, or extracted game assets.
- Public fingerprints identify revisions; they are not a source for game data.
- Derived artifacts containing substantial game data remain under `work/` and
  are not published automatically.
- Users must supply their own lawfully obtained dumps.

## Fidelity definition

A reconstruction is accepted when deterministic inputs demonstrate that it:

1. produces the same observable effects as the original routine;
2. preserves integer behavior, including overflow, signedness, and wraparound;
3. reproduces relevant memory and hardware accesses, or translates them through
   a documented interface;
4. passes repeatable comparisons against MAME traces; and
5. retains enough evidence for another contributor to repeat the test.
