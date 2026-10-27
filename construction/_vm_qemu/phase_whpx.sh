#!/bin/sh
# Machine virtuelle accelere par Hyper-V (WHPX), fenetre visible, sans redemarrage
# a chaud. Usage : phase_whpx.sh <iso> <d|c> [memoire Mo]
cd "$(dirname "$0")"
exec "/c/Program Files/qemu/qemu-system-x86_64.exe" -machine pc,acpi=off,hpet=off -accel whpx -m "${3:-1024}" \
  -drive file=win98.img,format=raw,if=ide,index=0 \
  -drive file="$1",media=cdrom,if=ide,index=2,readonly=on -boot "$2" -no-reboot \
  -vga cirrus -audiodev none,id=muet -device sb16,audiodev=muet -nic none -rtc base=localtime -display none \
  -monitor tcp:127.0.0.1:4444,server,nowait > qemu_whpx.log 2>&1
