#!/bin/sh
# Test de l'ISO WinMe_FR : apres la phase Hyper-V de Setup (copie), relance a froid la VM
# (tcg, ACPI) a chaque fermeture de QEMU (-no-reboot), CD de l'ISO dans le lecteur.
# Disque me_iso2.img, moniteur sur le port 4448 (QEMU_PORT=4448 python pilote.py ...),
# pour tourner en meme temps que la VM 98 (4444). Arret : fichier STOP_MEISO.
# Usage : me_iso_relance.sh <iso>
cd "$(dirname "$0")"
while tasklist | grep -qi qemu-system-x86_64; do
  netstat -an | grep -q "127.0.0.1:4448 .*LISTENING" || break
  sleep 10
done
while [ ! -f STOP_MEISO ]; do
  echo "$(date +%H:%M:%S) demarrage a froid ME (me_iso2.img)" >> me_relance.log
  "/c/Program Files/qemu/qemu-system-i386.exe" -machine pc -accel tcg -cpu pentium3 -m 512 \
    -drive file=me_iso2.img,format=raw,if=ide,index=0 \
    -drive file="$1",media=cdrom,if=ide,index=2,readonly=on -boot c -no-reboot \
    -vga cirrus -audiodev none,id=muet -device sb16,audiodev=muet -nic none -rtc base=localtime \
    -display none -monitor tcp:127.0.0.1:4448,server,nowait > qemu_meiso.log 2>&1
  sleep 5
done
