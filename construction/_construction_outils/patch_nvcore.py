# Correctif d'arret NVIDIA (rloew + Drugwash, MSFN 174096) pour NVCORE.VXD 80.xx
# et plus, meme methode que ShutdownPatcher 1.5.2.x, code "Full (c)" pour
# Windows 98 SE : l'appel de diffusion de message systeme (PUSH EBX / PUSH EAX /
# CALL) passe par une petite routine ajoutee en fin de premier objet, qui
# remplace les messages 04h, 25h et 32h par 52h avant d'appeler l'original.
# Usage : patch_nvcore.py <source> <destination>
import struct
import sys

CODE = bytes.fromhex("3C 04 74 08 3C 25 74 04 3C 32 75 02 B0 52 89 44 24 04 E9")

src, dst = sys.argv[1], sys.argv[2]
d = bytearray(open(src, "rb").read())
u16 = lambda o: struct.unpack_from("<H", d, o)[0]
u32 = lambda o: struct.unpack_from("<I", d, o)[0]
s32 = lambda o: struct.unpack_from("<i", d, o)[0]

off = u32(0x3C) if u16(0x18) >= 0x40 else 0x40
assert d[off:off + 2] == b"LE", "pas un VxD LE"
objtbl = off + u32(off + 0x40)
objsz = u32(objtbl)
newcode = u32(off + 0x80) + objsz        # fin des donnees du premier objet
call = newcode - 0x5C6                   # rel32 du CALL a detourner
assert d[call - 3:call] == bytes.fromhex("53 50 E8"), "code non reconnu ou deja corrige"
n = len(CODE) + 5                        # code + rel32 du saut + octet de taille
assert d[newcode:newcode + n] == bytes(n), "pas de place libre"
cible = call + 4 + s32(call)
d[call:call + 4] = struct.pack("<i", 0x5C2)
assert call + 4 + 0x5C2 == newcode
d[newcode:newcode + len(CODE)] = CODE
fin = newcode + len(CODE) + 4
d[fin - 4:fin] = struct.pack("<i", cible - fin)
d[fin] = n                               # taille, pour la restauration par ShutdownPatcher
struct.pack_into("<I", d, objtbl, objsz + n)
open(dst, "wb").write(d)
print("ok : appel %X -> routine %X -> cible %X, objet 1 %X -> %X"
      % (call - 1, newcode, cible, objsz, objsz + n))
