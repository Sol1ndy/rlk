# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# 「소생 실패」 (plan 3.4): strike 1 of 2 (the 2nd -> cb/lose); every organism bursts with no progress;
# walls cleared; the title; t20 the player takes 25 % max HP (non-lethal, no reaction); t60 the stage
# restarts at 2700 from wave 1.
scoreboard players add #apFail mb 1
scoreboard players set #apStage mb 0
execute if score #apFail mb matches 2.. run return run function rlk:boss/apep/svc/lose
function rlk:boss/apep/org/clear
function rlk:boss/apep/wall/clear
title @a[tag=player] title {text:"「소생 실패」",color:"#C36E5A"}
title @a[tag=player] subtitle {text:"다시 한 번 실패하면 쓰러집니다",color:"#C36E5A"}
scoreboard players set #apPLen mb 60
