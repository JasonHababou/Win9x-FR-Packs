@echo off
REM ============================================================
REM  MS Agent 2.0 pour Windows 9x + module de langue francais.
REM  Installeurs officiels Microsoft :
REM    MSAGENT.EXE  = moteur 2.00.0.2202 (Microsoft_Agent.iso,
REM                   "Microsoft Agent Core Components.zip"),
REM                   meme AGENTSVR.EXE que U98SESP3.66
REM    AGTX040C.EXE = langue FR 2.00.0.2115 (agt040c.dll)
REM  Le build 3427 (XP/Vista) a ete retire : il exige
REM  GetSystemDefaultUILanguage, absent du KERNEL32 de Windows 98.
REM  Enregistrement final au prochain demarrage (RunOnce Microsoft).
REM  Syntaxe COMMAND.COM. Appele par INSTALL.BAT APRES un "cd"
REM  dans ce dossier.
REM ============================================================
start /w MSAGENT.EXE /q:a /r:n
start /w AGTX040C.EXE /q:a /r:n
echo   - MS Agent 2.0 + langue francaise installes
