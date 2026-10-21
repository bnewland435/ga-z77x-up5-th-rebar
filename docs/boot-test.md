# One-time Ubuntu test

Status: successful override boot and 8 GB BAR confirmed October 2, 2026 at approximately 23:29 America/Chicago. Stability testing was subsequently concluded as stable by Bruce on October 21, 2026; see the completion report below.

This experimental file is specific to Pepper's supplied active DSDT. It is not a general Z77 override. A static check cannot establish that hardware forwards the advertised address range correctly. Failure may appear as an unsuccessful resize, missing devices, or a failed Linux boot.

Prerequisites observed: UEFI boot; CONFIG_ACPI_TABLE_UPGRADE=y; no Secure Boot support reported; EFI partition /dev/sda1 at /boot/efi. `/boot` was not reported as a separate mount.

Save artifacts/pepper-rebar.cpio in Downloads. Create a separate combined initramfs:

```bash
test_kernel=$(uname -r)
sudo sh -c 'cat "$1" "$2" > "$3"' sh \
  "$HOME/Downloads/pepper-rebar.cpio" \
  "/boot/initrd.img-$test_kernel" \
  "/boot/initrd.img-$test_kernel-rebar-test"
```

The early archive precedes the existing initramfs, as required by Linux's override documentation. This does not replace the original initramfs or modify GRUB defaults.

1. Reboot and tap Esc after the firmware screen to display GRUB.
2. Highlight the normal Ubuntu entry and press e.
3. Append `pci=realloc` to the linux line.
4. On the initrd line, append `-rebar-test` to the existing initrd.img filename. Preserve its directory and other filenames. Use the same kernel version as the file created above; select the corresponding entry under Advanced options if necessary.
5. Press Ctrl+X to boot.

If the test fails, restart and select the unchanged normal entry. These interactive edits apply to one boot only. Do not make the override permanent until confirmed working.

After boot:

```bash
sudo dmesg | grep -Ei 'ACPI.*(upgrade|override|DSDT)|root bus resource|BAR=|failed to resize'
sudo lspci -vv -s 03:00.0 | grep -A3 'Physical Resizable BAR'
cat /proc/cmdline
```

Required evidence: DSDT upgrade loaded; high root-bus window advertised; BAR 0 reports 8 GB; stable display and other devices. An enlarged window alone is not ReBAR success. If it fails, retain the full kernel log and inspect PCI bridge windows before trying more parameters.

The pre-test baseline was BAR 0 at c0000000, size 256 MB; BAR 2 at d0000000, size 2 MB; root memory window afa00000–feafffff; amdgpu VRAM=8144 MB and BAR=256 MB.

## Cleanup

Once finished, remove only the separate test initramfs for the kernel tested. Keep the normal initramfs. No BIOS restoration is required because this procedure never flashes firmware.

## Successful boot: October 2, 2026

Bruce supplied the following output after the one-time test on kernel 7.0.0-38-generic. `/proc/cmdline` included `pci=realloc`. The root filesystem UUID is omitted from this record.

```text
[    0.011704] ACPI: DSDT ACPI table found in initrd [kernel/firmware/acpi/DSDT.aml][0xa7db]
[    0.012203] ACPI: Table Upgrade: override [DSDT-ALASKA-   A M I]
[    0.012205] ACPI: DSDT 0x000000009DA99170 Physical table override, new table: 0x000000009D250000
[    0.012208] ACPI: DSDT 0x000000009D250000 00A7DB (v02 ALASKA A M I    00000013 INTL 20051117)
[    0.272013] pci_bus 0000:00: root bus resource [mem 0x850600000-0xfffffffff window]
[   10.160191] amdgpu 0000:03:00.0: [drm] Detected VRAM RAM=8144M, BAR=8192M
Capabilities: [200 v1] Physical Resizable BAR
    BAR 0: current size: 8GB, supported: 256MB 512MB 1GB 2GB 4GB 8GB
    BAR 2: current size: 2MB, supported: 2MB 4MB 8MB 16MB 32MB 64MB 128MB 256MB
```

This confirms that Linux loaded revision 0x13 of the DSDT, advertised the high window, and successfully resized BAR 0 from 256 MB to 8 GB. BAR 2 remains at 2 MB. No additional BIOS flash, Above 4G setup-variable write, or ReBarDxe insertion was performed for this test. Existing ME-cleaned F12 remains unchanged.

The desktop booted and Bruce returned terminal output. Extended GPU load, peripheral checks, suspend/resume, subsequent boots, persistence, and performance comparisons have not yet been reported. This success is specific to the tested combination.

### Original stability-check procedure (historical)

Use normal desktop graphics and video, check USB/audio/network/storage, and run a familiar GPU workload for 10–15 minutes. Then inspect:

```bash
sudo dmesg | grep -Ei 'amdgpu.*(error|fail|timeout|reset|fault)|AER:|PCIe Bus Error'
sudo lspci -vv -s 03:00.0 | grep -A3 'Physical Resizable BAR'
```

At the time of the original one-boot test, no persistence changes had been made; the interactive GRUB edits applied only to that boot.

## Stability testing concluded: October 21, 2026

Bruce reports that testing following the Resizable BAR changes has concluded and Pepper is stable. This completes the stability-testing phase for the documented GA-Z77X-UP5 TH and Radeon RX 9060 XT 8 GB system.

This is an owner-reported operational result. The October 2 boot evidence above remains the recorded confirmation of the 8 GB BAR. No new diagnostic logs, itemized peripheral or suspend/resume results, or controlled performance comparisons accompany the completion report. No performance gain or validation on other systems is claimed.
