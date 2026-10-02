# F12 image analysis

Input: `up5-th-me-cleaned-candidate(1).bin`, 8,388,608 bytes.

SHA-256: `c53da7f97f768107d36200e2f483aa42f5997768aa65eb50d6ed8ec963e09318`.

Board identifiers found: `Z77XUP5TH.F1212` at 0x76c650 and `Z77X-UP5 TH` at 0x791fa4.

The descriptor reports descriptor 0x000000–0x000fff, GbE 0x001000–0x002fff, ME 0x003000–0x1fffff, and a BIOS region spanning 0x000000–0x7fffff. The unusual overlapping BIOS descriptor range is recorded as observed, not normalized or endorsed. A fresh chip read is needed to prove identity with the running image.

ME manifest version: 8.1.0.1248. FPT contains one partition, FTPR, offset 0x93000 relative to the ME region, size 0x75000. Only 63,306 bytes in that partition are non-FF. These observations are consistent with cleaning; they do not independently establish runtime ME disablement. Bruce reports this candidate was the image flashed.

UEFI modules were extracted with uefi_firmware 1.16. IFR was decoded with IFRExtractor-RS 1.6.1. Names assigned by a parser's GUID database (including unrelated vendor labels) are not proof of firmware provenance.

## Exact unmodified pattern matches

Offsets below are relative to the extracted PE image, not the full SPI binary. Do not patch the full binary at these offsets.

| Module | Published patch purpose | PE offset |
|---|---|---|
| PciHostBridge, 8D6756B9-E55E-4D6A-A3A5-5E4D72DDF772 | Remove <4 GB BAR limit in SubmitResources | 0x0edb |
| PciHostBridge | Replace fixed 16 GiB MMIO region with use of 36-bit address space | 0x13c6 |
| PciHostBridge | Remove 4 GB limit for PciRootBridgeIo.Mem, 771B variant | 0x1775 |
| PciBus, 3C1DE39F-D207-408A-AACC-731CFB7F1DD7 | Remove <16 GB BAR limit | 0x8808 |

The tested AddMemorySpace and one BAR-downgrade pattern did not match. That does not establish absence of related limitations: different machine code may implement them. IvyUSB3 applicability has not been byte-verified. No patches have been applied to the firmware.

## Above 4G Decoding

IFR question 0x12, VarStoreId 0x1, variable `Setup`, GUID EC87D643-EBA4-4BB5-A1E5-3F3E36B20DA9, variable size 0x498, byte offset 0x03. Disabled is 0 (default), enabled is 1. Form 0x404 has an empty title. Presence in IFR does not prove the setting is exposed in the normal menu or currently enabled.

CSM Support is also present in IFR at Setup offset 0x457. Its runtime state has not been read.

Related Gigabyte Z77X-UD5H success appears in the ReBarUEFI tested-board list; it does not validate this exact UP5 TH / F12 / RX 9060 XT combination.
