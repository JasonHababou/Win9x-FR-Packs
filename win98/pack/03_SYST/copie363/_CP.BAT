@echo off
REM ============================================================
REM  _CP.BAT FICHIER DOSSIER - appele par copie.bat (meme dossier).
REM  Remplace DOSSIER\FICHIER par la version 3.63 du dossier courant
REM  SEULEMENT s'il existe deja (comme SP3.0, drapeau 1056) : on
REM  n'installe pas un composant absent (ex. SNMP non installe).
REM  L'original est sauvegarde une seule fois dans C:\W98FR\BAK.
REM ============================================================
if not exist %2\%1 goto FIN
if not exist C:\W98FR\BAK\%1 copy %2\%1 C:\W98FR\BAK > NUL
copy %1 %2 > NUL
echo   - %1 remplace dans %2
:FIN
