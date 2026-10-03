# GA-Z77X-UP5 TH Resizable BAR research

Research on enabling an 8 GiB VRAM BAR for a Gigabyte Radeon RX 9060 XT 8 GB on Bruce's Ubuntu computer, Pepper.

**Status, October 2, 2026: successful Ubuntu boot with an 8 GB BAR confirmed on kernel 7.0.0-38-generic using the DSDT override and `pci=realloc`. No BIOS flash or ReBarDxe insertion was needed. Stability, performance comparisons, and persistence remain pending.**

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

## Next steps

1. Check normal graphics, video, USB, audio, networking, storage, and a GPU workload.
2. Inspect kernel logs for GPU faults, resets, or PCI errors.
3. Make the successful Linux override persistent with a recoverable normal boot path after stability checks.
4. Measure performance separately; no improvement has yet been established.
5. Firmware modification is unnecessary for the demonstrated Linux result.

## Sources

- [ReBarUEFI](https://github.com/xCuri0/ReBarUEFI)
- [Patch definitions](https://github.com/xCuri0/ReBarUEFI/blob/master/UEFIPatch/patches.txt)
- [Hidden Above 4G settings](https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding)
- [DSDT patching](https://github.com/xCuri0/ReBarUEFI/wiki/DSDT-Patching)
- [Ivy Bridge USB patch](https://github.com/xCuri0/ReBarUEFI/blob/master/UEFIPatch/IvyUSB3.txt)
- [Linux ACPI initrd table override](https://docs.kernel.org/admin-guide/acpi/initrd_table_override.html)

[Recorded boot evidence](docs/boot-test.md#successful-boot-october-2-2026) confirms table loading, a high root window, and an 8 GB BAR on this system. Long-term stability, other systems, and performance gains are not yet validated.
