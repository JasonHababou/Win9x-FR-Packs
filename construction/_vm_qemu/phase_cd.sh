#!/bin/sh
# Demarrage sur le CD, sans redemarrage a chaud (QEMU se ferme au redemarrage).
cd "$(dirname "$0")"
exec "/c/Program Files/qemu/qemu-system-i386.exe" -machine pc,acpi=off,hpet=off -cpu pentium3 -m "${2:-1024}" -accel tcg \
  -drive file=win98.img,format=raw,if=ide,index=0 \
  -drive file="$1",media=cdrom,if=ide,index=2,readonly=on -boot d -no-reboot \
  -vga cirrus -audiodev none,id=muet -device sb16,audiodev=muet -nic none -rtc base=localtime -display none \
  -monitor tcp:127.0.0.1:4444,server,nowait > qemu.log 2>&1
