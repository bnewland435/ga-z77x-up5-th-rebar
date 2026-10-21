# GA-Z77X-UP5 TH Resizable BAR research

Research on enabling an 8 GiB VRAM BAR for a Gigabyte Radeon RX 9060 XT 8 GB on Bruce's Ubuntu computer, Pepper.

**Status, October 21, 2026: stability testing has concluded. Bruce reports Pepper is stable following the Resizable BAR changes. The previously documented 8 GB BAR was enabled on kernel 7.0.0-38-generic using the DSDT override and `pci=realloc`, without an additional BIOS flash or ReBarDxe insertion. This is an owner-reported stability result for this system; a measured performance improvement has not been established.**

## System

| Component | Configuration |
|---|---|
| Motherboard | Gigabyte GA-Z77X-UP5 TH |
| CPU / RAM | Core i7-3770K / 32 GB DDR3 |
| Firmware | F12; user reports the running image was rewritten with cleaned/disabled Intel ME |
| GPU | Gigabyte RX 9060 XT 8 GB, PCI 0000:03:00.0, subsystem 2430 |
| OS | Ubuntu 26.04; amdgpu; UEFI boot |
| Secure Boot | mokutil reports system does not support Secure Boot |
| ACPI override support | CONFIG_ACPI_TABLE_UPGRADE=y |

## Findings

The GPU explicitly advertises BAR 0 sizes of 256 MB, 512 MB, 1 GB, 2 GB, 4 GB, and 8 GB. Before the test, BAR 0 was 256 MB; after the test it is 8 GB. BAR 2 is 2 MB and has its own independent size capabilities. The successful test's amdgpu log reports 8144 MB VRAM and an 8192 MB BAR. Enlarging a BAR does not add VRAM.

The supplied F12 candidate contains an Above 4G Decoding setup question in the `Setup` variable at offset `0x03`, with disabled=0 and enabled=1. This is a static IFR finding, not verification of its runtime value or effect. UEFI boot does not prove CSM is disabled. Do not write a setup variable using a generic command without checking the variable identity and firmware.

Its decompressed PCI modules contain exact matches for published ReBarUEFI patch patterns. The active DSDT contains a conditional high memory window with a fixed 16 GiB length. Baseline kernel logs advertised no memory window above 4 GiB. The override boot advertises `0x850600000–0xfffffffff`.

See [firmware analysis](docs/firmware-analysis.md), [DSDT changes](docs/dsdt-analysis.md), and [one-boot test](docs/boot-test.md).

## Files

- `artifacts/pepper-original-dsdt.aml`: active DSDT supplied by Bruce.
- `artifacts/pepper-rebar-dsdt.aml`: experimental override, not firmware to flash.
- `artifacts/pepper-rebar.cpio`: early initramfs archive containing the override.
- `tools/build_override.py`: reproduces the modified AML and archive using Python's standard library.

Full SPI firmware images are excluded: they can contain machine-specific identifiers, configuration, and vendor firmware. The supplied firmware's identity and analysis are recorded instead.

## Testing concluded: stable

On October 21, 2026, Bruce reported that testing following the Resizable BAR changes has concluded and the system is stable. This closes the stability-testing item for Pepper's documented GA-Z77X-UP5 TH / RX 9060 XT configuration.

The original boot evidence and test procedure are retained in [the test record](docs/boot-test.md). The completion report does not include a new kernel-log capture, an itemized peripheral or suspend/resume test matrix, or a controlled before/after benchmark. Performance comparisons remain separate from the reported stability result. Results on other systems remain unvalidated.

## Sources

- [ReBarUEFI](https://github.com/xCuri0/ReBarUEFI)
- [Patch definitions](https://github.com/xCuri0/ReBarUEFI/blob/master/UEFIPatch/patches.txt)
- [Hidden Above 4G settings](https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding)
- [DSDT patching](https://github.com/xCuri0/ReBarUEFI/wiki/DSDT-Patching)
- [Ivy Bridge USB patch](https://github.com/xCuri0/ReBarUEFI/blob/master/UEFIPatch/IvyUSB3.txt)
- [Linux ACPI initrd table override](https://docs.kernel.org/admin-guide/acpi/initrd_table_override.html)

[Recorded boot evidence](docs/boot-test.md#successful-boot-october-2-2026) confirms table loading, a high root window, and an 8 GB BAR on this system. Stability testing is now concluded as stable according to Bruce's October 21 report. Other systems and performance gains remain unvalidated.
