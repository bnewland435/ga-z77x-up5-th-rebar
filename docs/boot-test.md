# One-time Ubuntu test

Status: instructions supplied; execution and results have not yet been reported.

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

The current baseline is BAR 0 at c0000000, size 256 MB; BAR 2 at d0000000, size 2 MB; root memory window afa00000–feafffff; amdgpu VRAM=8144 MB and BAR=256 MB.

## Cleanup

Once finished, remove only the separate test initramfs for the kernel tested. Keep the normal initramfs. No BIOS restoration is required because this procedure never flashes firmware.
