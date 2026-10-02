# GA-Z77X-UP5 TH Resizable BAR research

Research on enabling an 8 GiB VRAM BAR for a Gigabyte Radeon RX 9060 XT 8 GB on Bruce's Ubuntu computer, Pepper.

**Status, October 2, 2026: static analysis and Linux test archive completed. Boot test pending. No successful large BAR, performance gain, or modified BIOS flash has been demonstrated.**

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

The GPU explicitly advertises BAR 0 sizes of 256 MB, 512 MB, 1 GB, 2 GB, 4 GB, and 8 GB. Its current BAR 0 is 256 MB. BAR 2 is 2 MB and has its own independent size capabilities. The amdgpu log reports 8144 MB VRAM and a 256 MB BAR. Enlarging a BAR does not add VRAM.

The supplied F12 candidate contains an Above 4G Decoding setup question in the `Setup` variable at offset `0x03`, with disabled=0 and enabled=1. This is a static IFR finding, not verification of its runtime value or effect. UEFI boot does not prove CSM is disabled. Do not write a setup variable using a generic command without checking the variable identity and firmware.

Its decompressed PCI modules contain exact matches for published ReBarUEFI patch patterns. The active DSDT contains a conditional high memory window with a fixed 16 GiB length. Current kernel root-bus logs advertise no memory window above 4 GiB.

See [firmware analysis](docs/firmware-analysis.md), [DSDT changes](docs/dsdt-analysis.md), and [one-boot test](docs/boot-test.md).

## Files

- `artifacts/pepper-original-dsdt.aml`: active DSDT supplied by Bruce.
- `artifacts/pepper-rebar-dsdt.aml`: experimental override, not firmware to flash.
- `artifacts/pepper-rebar.cpio`: early initramfs archive containing the override.
- `tools/build_override.py`: reproduces the modified AML and archive using Python's standard library.

Full SPI firmware images are excluded: they can contain machine-specific identifiers, configuration, and vendor firmware. The supplied firmware's identity and analysis are recorded instead.

## Next steps

1. Test the separate initramfs with a one-time GRUB edit.
2. Confirm that the override loaded and a high PCI memory window appeared.
3. Confirm whether BAR 0 becomes 8 GB and that the GPU and other devices function.
4. If allocation fails, inspect complete boot logs and bridge windows before changing anything further.
5. Only consider firmware patches after verifying the running SPI image and a recovery path. Preserve ME, descriptor, and GbE changes.

## Sources

- [ReBarUEFI](https://github.com/xCuri0/ReBarUEFI)
- [Patch definitions](https://github.com/xCuri0/ReBarUEFI/blob/master/UEFIPatch/patches.txt)
- [Hidden Above 4G settings](https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding)
- [DSDT patching](https://github.com/xCuri0/ReBarUEFI/wiki/DSDT-Patching)
- [Ivy Bridge USB patch](https://github.com/xCuri0/ReBarUEFI/blob/master/UEFIPatch/IvyUSB3.txt)
- [Linux ACPI initrd table override](https://docs.kernel.org/admin-guide/acpi/initrd_table_override.html)

Patch-pattern matches and successful AML decoding are not hardware validation. This override advertises address space; it does not itself prove chipset routing, bridge allocation, or driver resizing will succeed.
