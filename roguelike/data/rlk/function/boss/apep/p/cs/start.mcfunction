# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# The CS (plan 7.7): every organism bursts, walls cleared, libraries cleared, cine; the success line.
function rlk:boss/apep/svc/phase_cs
scoreboard players set #apStage mb 0
function rlk:boss/apep/org/clear
function rlk:boss/apep/wall/clear
function rlk:boss/apep/svc/lib_clear
function rlk:boss/apep/svc/cine_on
function rlk:mboss/line/say {t:"오아시스의 심장이 소생했습니다",c:"#EDCF63",gap:2,hold:60,snd:2}
scoreboard players set #apPLen mb 192
