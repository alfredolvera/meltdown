# Meltdown

Meltdown is a research and learning project exploring native recompilation of
the 1994 **Killer Instinct** arcade game. The first target is PC; a Nintendo 64
port may follow once the native core is understood, testable, and sufficiently
platform-independent.

This is not a matching decompilation. The project does not aim to recover the
original source verbatim, reproduce the original compiler, or generate a
byte-identical ROM. Its purpose is to recover as much authentic MIPS R4600 game
logic as practical and run it natively through verified decompilation, static
recompilation, or a combination of both. New code is limited to tooling, tests,
and explicit replacements for arcade hardware and host-platform services.

## Current status

- Working revision confirmed as **KI v1.5d**. The main boot ROM and all eight
  audio ROMs match the MAME manifest, and `chdman` fully verified the CHD.
- MAME 0.289 and Ghidra 12.1.3 are installed and scripted on Linux.
- Boot ROM, RAM snapshots, and an initial 100 ms execution trace were captured.
- The U98 compressed payload was extracted into three segments and compared
  with MAME RAM. The segment containing the main loop matches byte-for-byte.
- The provisional main controller at `0x8802aa24` and recurring loop head at
  `0x8802ae14` have provenance records and seeded Ghidra labels.
- A minimal R4600 memory model runs in the native PC test harness.
- Next milestone: select a small, bounded original routine and execute it
  natively against fixtures captured from MAME.

## Game data

No ROMs, CHDs, extracted graphics, audio, memory dumps, or other copyrighted
game data are included. Users must provide their own lawfully obtained dumps.
All local inputs and substantial derived artifacts remain ignored by Git.

## Quick start

From the repository root:

```sh
make check
python3 tools/ki_project.py doctor
python3 tools/ki_project.py inventory /path/to/your/KI-files \
  --output work/input-inventory.json
```

`inventory` reads files, calculates fingerprints, and compares ZIP/CHD members
with the public MAME manifest. It never modifies the supplied dumps.

To create a provenance record for an identified function:

```sh
python3 tools/ki_project.py new-function \
  --id ki15d_80001234 \
  --address 0x80001234 \
  --name provisional_name
```

## Documentation

1. [Project charter](docs/PROJECT_CHARTER.md)
2. [Proof-of-concept roadmap](docs/ROADMAP.md)
3. [Initial hardware map](docs/HARDWARE_BASELINE.md)
4. [Verification method](docs/VERIFICATION.md)
5. [Ghidra project](docs/GHIDRA.md)
6. [External references](docs/EXTERNAL_REFERENCES.md)
7. [Decision log](docs/DECISIONS.md)
8. [Work log](docs/WORKLOG.md)

## Repository layout

```text
config/                 Public fingerprints and revision configuration
docs/                   Scope, technical notes, decisions, and work log
ghidra_scripts/         Reproducible labels and analysis setup
mame/                   Debugger capture and tracing scripts
native/                 Native PC runtime and tests
provenance/             One JSON record per recovered original function
tools/                  Inventory, comparison, and validation utilities
work/                   Local captures and analysis; always ignored by Git
```

## Disclaimer

Meltdown is an unofficial, non-commercial research project. It is not affiliated
with or endorsed by Rare, Microsoft, Nintendo, Midway, or MAME. Killer Instinct
and all related game assets remain the property of their respective owners.
