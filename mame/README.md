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

Dumps, traces, and disassembly never enter Git.

Although MAME's map displays physical ranges, `save` and `dasm` accept R4600
virtual addresses. These scripts use KSEG0/KSEG1 for RAM and `0xbfc00000` for
the boot vector.
