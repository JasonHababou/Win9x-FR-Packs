@echo off
REM ISO WinMeFR : lance par WMEFRDOS.BAT sous COMMAND /F (echec automatique au
REM lieu de "Abandon, Reprise, Echec"). C: formatee = un fichier ecrit sur C: se
REM recopie sur le disque virtuel (COK.TXT). Sur une partition non formatee, IF
REM EXIST C:\NUL et IF EXIST apres un echec repondaient "vrai" (tests QEMU
REM 2026-10-26) : COPY, lui, ne cree rien quand la lecture echoue.
echo ok> C:\WMEFRTST.TMP
copy C:\WMEFRTST.TMP %1:\COK.TXT > NUL
del C:\WMEFRTST.TMP > NUL
