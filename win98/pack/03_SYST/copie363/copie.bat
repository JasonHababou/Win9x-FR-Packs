@echo off
REM ============================================================
REM  Fichiers ou U98SESP3.63 est plus recent que SP3.0 B4 FR
REM  (tous EN dans les deux versions : aucune regression FR).
REM  Syntaxe COMMAND.COM. Appele par INSTALL.BAT APRES un "cd"
REM  dans ce dossier : les sources sont dans le dossier courant.
REM  Chaque fichier n'est remplace que s'il existe deja (_CP.BAT),
REM  dans le dossier ou SP3.0 et 3.66 le placent :
REM    WINDOWS\SYSTEM : DUNZIP32, DZIP32, HHSETUP, ITIRCL, ITSS
REM    WINDOWS        : HH.EXE, SNMP.EXE, SNMPAPI.DLL
REM    Fichiers communs\Microsoft Shared\TextConv : MSCONV97.DLL
REM  SNMPAPI.DLL 5.0.2195.6811 est indispensable au SNMP.EXE 3.63.
REM  Retires le 2026-10-13 (regression FR vers EN, ou identiques
REM  a SP3.0) : HYPERTRM.*, HTICONS, HTML32.CNV, XENROLL, JSCRIPT,
REM  HHCTRL.OCX, SSDPAPI, SSDPSRV, UPNP.
REM ============================================================
call _CP.BAT DUNZIP32.DLL %WINDIR%\SYSTEM
call _CP.BAT DZIP32.DLL %WINDIR%\SYSTEM
call _CP.BAT HHSETUP.DLL %WINDIR%\SYSTEM
call _CP.BAT ITIRCL.DLL %WINDIR%\SYSTEM
call _CP.BAT ITSS.DLL %WINDIR%\SYSTEM
call _CP.BAT HH.EXE %WINDIR%
call _CP.BAT SNMP.EXE %WINDIR%
call _CP.BAT SNMPAPI.DLL %WINDIR%
call _CP.BAT MSCONV97.DLL C:\PROGRA~1\FICHIE~1\MICROS~1\TEXTCONV
