# Work log

## 2026-09-03 — Project initialization

- Formalized the PC → N64 scope and the boundary between original logic and
  hardware shims.
- Selected KI v1.5d as the provisional target.
- Recorded public fingerprints for the U98, DCS audio ROMs, and v1.5d CHD.
- Documented the initial hardware map from the official MAME driver.
- Created dependency-free tooling for diagnostics, inventory, and provenance.
- Added a minimal R4600 memory model and native tests.
- Initial diagnostics found Python, GCC, and Make; MAME and Ghidra were later
  located or installed through Flatpak.

### Initial next steps

1. Inventory the available dumps without copying them into the repository.
2. Install or locate MAME and Ghidra.
3. Pin versions and save `mame -listxml kinst`.
4. Start KI under the debugger and capture the first verifiable map and snapshot.

## 2026-09-03 — Dump identification

- `kinst.zip`: v1.5d main ROM and all eight DCS ROMs matched, 9/9.
- `kinst.chd`: CHD v5 with 131,076,608 logical bytes and combined SHA-1
  `81d833236e994528d1482979261401b198d1ca53`, matching MAME.
- The complete local inventory was written to `work/input-inventory.json`; all
  dumps remain ignored by Git.
- Header identity was established first; complete hunk verification followed.

### Verification completed

- MAME 0.289 was already available through Flatpak.
- `chdman verify` 0.289 confirmed both the raw-data and overall SHA-1 values.
- KI v1.5d ran for 15 emulated seconds in benchmark mode without errors, at an
  average speed of approximately 1,060%.

## 2026-09-03 — First dynamic map and code origin

- Captured all 8 MiB of main RAM after ten seconds and a 100 ms execution trace
  with MAME 0.289.
- The trace identified the provisional main controller at `0x8802aa24` and its
  recurring loop head at `0x8802ae14`.
- Installed and automated Ghidra 12.1.3 through Flatpak.
- Created `work/ghidra/ki15d` with U98 and main RAM, architecture
  `MIPS:LE:64:64-32addr:n32`, and verified entry-point labels.
- Examined `nekuz0r/ki-rom` at commit
  `8e4344cfd2b039e2ca97c9f115bb8f1acaff804b` without adding it to version
  control.
- Its `kipack` passed 14/14 synthetic tests and extracted three segments from
  the verified U98. Two match RAM completely; the third retains 331,098 of
  332,032 bytes after ten seconds of activity.
- This evidence corrected the initial hypothesis: the main executable arrives
  compressed in U98, while the disk supplies later data and assets.

## 2026-09-03 — Public project identity

- Renamed the project **Meltdown**.
- Defined it as a research and learning project focused on native recompilation,
  with PC as the first target.
- Clarified that a matching decompilation, original compiler, and byte-identical
  ROM are explicitly outside the project goals.
- Converted public documentation and user-facing tooling to English before the
  first GitHub publication.
