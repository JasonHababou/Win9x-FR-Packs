#!/bin/sh
# Relance a froid la VM de test QuickInstall (disque, tcg) a chaque fermeture de QEMU
# (-no-reboot). Arret : fichier STOP_QI. Journal : qi_relance.log
cd "$(dirname "$0")"
while [ ! -f STOP_QI ]; do
  echo "$(date +%H:%M:%S) demarrage a froid QI" >> qi_relance.log
  ./phase_qi.sh c tcg "$1"
  sleep 5
done
