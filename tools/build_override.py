#!/usr/bin/env python3
"""Reproduce Pepper's experimental override; never flashes firmware."""
import hashlib
from pathlib import Path
import struct

root = Path(__file__).resolve().parents[1]
original = (root / 'artifacts/pepper-original-dsdt.aml').read_bytes()
assert hashlib.sha256(original).hexdigest() == '024c90405ab5b70d3981a317cd29b14c9de974e9e1aa54267ae420992fa838f4', 'Unexpected input DSDT'
table = bytearray(original)
changes = [
    (0x1797, '91934d4d36340092944f5359530bd307', '92930e00000000000000000c00000000'),
    (0x17e0, '700e00000000040000004d324c4e', '700effffffff0f0000004d324d58'),
    (0x1814, '74724d324d4e4d324c4e00014d324d58', '72744d324d584d324d4e00014d324c4e'),
]
for offset, before, after in changes:
    before, after = bytes.fromhex(before), bytes.fromhex(after)
    assert len(before) == len(after)
    assert table[offset:offset + len(before)] == before
    table[offset:offset + len(after)] = after
struct.pack_into('<I', table, 24, struct.unpack_from('<I', table, 24)[0] + 1)
table[9] = 0
table[9] = (-sum(table)) & 255
assert len(table) == len(original) and sum(table) % 256 == 0
assert sum(a != b for a, b in zip(original, table)) == 29
(root / 'artifacts/pepper-rebar-dsdt.aml').write_bytes(table)
archive = bytearray()

def entry(name, data, inode):
    name = name.encode() + b'\0'
    fields = [inode, 0o100644, 0, 0, 1, 0, len(data), 0, 0, 0, 0, len(name), 0]
    archive.extend(b'070701' + ''.join(f'{x:08x}' for x in fields).encode() + name)
    archive.extend(b'\0' * ((-len(archive)) % 4))
    archive.extend(data)
    archive.extend(b'\0' * ((-len(archive)) % 4))

entry('kernel/firmware/acpi/DSDT.aml', table, 1)
entry('TRAILER!!!', b'', 2)
archive.extend(b'\0' * ((-len(archive)) % 512))
assert hashlib.sha256(archive).hexdigest() == '35940be41d54e50d294c7375b94098cdeb328c7e6de3b2c729ce706a6236372c'
(root / 'artifacts/pepper-rebar.cpio').write_bytes(archive)
print('Reproduced AML and early archive; boot validation remains pending.')
