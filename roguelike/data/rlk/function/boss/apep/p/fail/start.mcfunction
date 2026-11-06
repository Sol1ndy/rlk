# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# 「소생 실패」 (plan 3.4): strike 1 of 2 (the 2nd -> cb/lose: the death path; a Ronova revive restarts the stage at t60);
# every organism bursts with no progress; walls cleared; the Heart withers; the shock ring; the title + the instant-kill
# warning; t20 the player takes 25 % max HP (non-lethal, no reaction; not after a lose); t60 the stage restarts at
# 2700 from wave 1 (no hint line: the no-tips rule).
scoreboard players add #apFail mb 1
scoreboard players set #apStage mb 0
scoreboard players set #apq40L mb 0
scoreboard players set #apHudQ mb 1
execute if score #apFail mb matches 2.. run scoreboard players set #apq40L mb 1
function rlk:boss/apep/org/burst_all
function rlk:boss/apep/org/clear
function rlk:boss/apep/wall/clear
function rlk:boss/apep/svc/lib_clear
function rlk:boss/apep/om/heart/play/heart_wither
execute positioned 440 201 8 run function rlk:boss/apep/fx/p/shock_ring
execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/fail_strike
execute if score #apq40L mb matches 0 run function rlk:boss/apep/p/fail/warn
execute if score #apq40L mb matches 1 run function rlk:boss/apep/fx/hud/title {g:"fail",t:"「소생 실패」",c:"#C36E5A",s:"",hold:50}
scoreboard players set #apPLen mb 60
execute if score #apq40L mb matches 1 run function rlk:boss/apep/svc/lose
