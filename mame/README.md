# MAME automation

The detected installation is MAME 0.289 through Flatpak. Scripts in this
directory run from the repository root and write exclusively under `work/`.

`capture_boot.cmd` runs for ten emulated seconds and captures:

- the memory map exposed by MAME for the main CPU;
- 512 KiB of low RAM;
- 8 MiB of main RAM; and
- the 512 KiB boot ROM.

The ROM assembly is generated afterward with `unidasm mips3le`, included in the
same MAME distribution. `trace_postboot.cmd` records ten milliseconds of the
main CPU after waiting ten emulated seconds.

`trace_postboot_100ms.cmd` covers approximately six frames. It confirms which
block recurs as the main coordinator before a name is added to its provenance
record.

`oracle_ki15d_8802d5b0.cmd` loads the verified extracted segment and executes
the original routine at `0x8802d5b0` with controlled inputs. Run it from the
repository root with MAME's dynamic recompiler disabled:

```sh
flatpak run org.mamedev.MAME kinst \
  -rompath assets/ki1 \
  -debug -nodrc \
  -debugscript mame/oracle_ki15d_8802d5b0.cmd \
  -video none -sound none -nothrottle -skip_gameinfo -seconds_to_run 3 \
  -cfg_directory work/mame/cfg -diff_directory work/mame/diff
```

The compact input/output results are tracked in
`tests/fixtures/ki15d_8802d5b0.csv`; the instruction trace remains under
`work/` and is never committed.

`oracle_ki15d_8800700c.cmd` applies the same method to a small RAM-writing leaf
routine. It records the source and destination before and after three controlled
calls. Its compact results live in `tests/fixtures/ki15d_8800700c.csv`; the
native test uses them to build and compare the complete expected RAM image.

Memory dumps, traces, and full generated disassemblies never enter Git. Small
per-function assembly excerpts may be tracked when they are required for
provenance and do not contain game assets.

Although MAME's map displays physical ranges, `save` and `dasm` accept R4600
virtual addresses. These scripts use KSEG0/KSEG1 for RAM and `0xbfc00000` for
the boot vector.
