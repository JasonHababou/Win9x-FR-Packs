#!/bin/sh
# Test d'une ISO QuickInstall dans une VM neuve : disque qi_test.qcow2 (vierge), CD = ISO QI,
# moniteur 4447 (QEMU_PORT=4447 python pilote.py ...). Son coupe, pas de reseau.
# Usage : phase_qi.sh <d|c> <whpx|tcg> <iso> [memoire Mo]
cd "$(dirname "$0")"
[ -f qi_test.qcow2 ] || "/c/Program Files/qemu/qemu-img.exe" create -f qcow2 qi_test.qcow2 8G
if [ "$2" = whpx ]; then Q="/c/Program Files/qemu/qemu-system-x86_64.exe"; A="-accel whpx"
else Q="/c/Program Files/qemu/qemu-system-i386.exe"; A="-accel tcg -cpu pentium3"; fi
exec "$Q" -machine pc $A -m "${4:-512}" \
  -drive file=qi_test.qcow2,format=qcow2,if=ide,index=0 \
  -drive file="$3",media=cdrom,if=ide,index=2,readonly=on -boot "$1" -no-reboot \
  -vga cirrus -audiodev none,id=muet -device sb16,audiodev=muet -nic none -rtc base=localtime -display none \
  -monitor tcp:127.0.0.1:4447,server,nowait > qemu_qi.log 2>&1
