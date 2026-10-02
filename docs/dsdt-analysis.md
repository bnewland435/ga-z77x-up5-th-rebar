# Active DSDT and experimental override

Original SHA-256: `024c90405ab5b70d3981a317cd29b14c9de974e9e1aa54267ae420992fa838f4`.

Length: 42,971 bytes. ACPI checksum: valid. OEM ID `ALASKA`, OEM table ID `A M I` padded with NULs, OEM revision 0x12.

The active table has the same length as the DSDT embedded in the supplied F12 image, with 26 differing bytes. Runtime address fixups are a plausible explanation, but this is not proof that the full SPI images match.

The PCI0 `_CRS` method has an existing QWordMemory descriptor. It zeroes the descriptor length if `MM64 == 0` or `OSYS <= 0x07D3`. Otherwise it starts the window at `TUUD << 20` when TUUD >= 0x1000, or at 4 GiB. It sets a fixed length of 16 GiB and computes the maximum from the minimum and length.

The supplied kernel logs contain no high root window. This is consistent with the conditional suppression branch, but the actual MM64 value was not read.

## Experimental changes

Three equal-length AML substitutions preserve all package offsets and the table size:

| AML offset | Change |
|---|---|
| 0x1797 | Replace the MM64/OSYS suppression predicate with an always-false expression, so the existing high window is exposed |
| 0x17e0 | Assign M2MX = 0x0000000FFFFFFFFF instead of assigning M2LN = 16 GiB |
| 0x1814 | Calculate M2LN = (M2MX - M2MN) + 1 instead of M2MX = (M2MN + M2LN) - 1 |

The original TUUD-based minimum is retained. OEM revision is incremented to 0x13 for Linux's table-upgrade selection. The checksum is recalculated. In total, 29 bytes change, including header bytes.

The resulting table was independently disassembled by iASL 20230628; the intended expressions were confirmed. Table length and checksum were checked. Recompiling the original decompiled source produced two pre-existing errors, so source recompilation was not used; no unrelated AML or device IDs were repaired.

The 64 GiB figure is the platform address-space ceiling, not requested GPU memory and not a new 64 GiB BAR. The GPU's target BAR is 8 GiB. No BIOS code or ME region is changed by this Linux override.

The early archive contains `kernel/firmware/acpi/DSDT.aml` in uncompressed newc format. Archive SHA-256: `35940be41d54e50d294c7375b94098cdeb328c7e6de3b2c729ce706a6236372c`.
