# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# T1 t106: the Heart objective: its title (FN-6 + the kit title line), the gold progress, music 2, the
# ley-line dressing, the stage markers.
function rlk:boss/apep/svc/title_heart
function rlk:boss/apep/fx/hud/title {g:"heart",t:"「오아시스의 심장」",c:"#EDCF63",s:"",hold:50}
execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/t1_hud
execute positioned 440 201 8 run function rlk:boss/apep/fx/dress/ley {n:7}
function rlk:boss/apep/svc/music_2
scoreboard players set #apHt mb 2700
function rlk:boss/apep/org/marks
scoreboard players set #apHudQ mb 1
