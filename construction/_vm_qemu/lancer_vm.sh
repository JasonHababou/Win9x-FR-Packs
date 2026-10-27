#!/bin/sh
# Lance la machine virtuelle de test (sans fenetre, pilotee par pilote.py).
# Usage : lancer_vm.sh <iso> <d|c> [memoire Mo]
cd "$(dirname "$0")"
exec "/c/Program Files/qemu/qemu-system-i386.exe" -machine pc,acpi=off,hpet=off -cpu pentium3 -m "${3:-1024}" -accel tcg \
  -drive file=win98.img,format=raw,if=ide,index=0 \
  -drive file="$1",media=cdrom,if=ide,index=2,readonly=on -boot "$2" \
  -vga cirrus -device sb16 -nic none -rtc base=localtime -display none \
  -monitor tcp:127.0.0.1:4444,server,nowait > qemu.log 2>&1
