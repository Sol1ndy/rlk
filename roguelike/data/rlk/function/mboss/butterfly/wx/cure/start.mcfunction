# 달빛 고치 cured (the core's coc/cure, at the player's body): S5 tick 0, then the clock.
scoreboard players set #bpS5T mb 1
# t0 (the cure tick): the kit's cure (gold beam 0-8, burst + ring from 6, emblem from 11) around the shoulder-view
# avatar; in first person (the player is rlk_body: the camera-facing cards would sit on the eyes) only the gold
# ring spreading on the floor (fix PL-1; the reward pop owns the title line). The chime recipe either way.
execute if entity @e[tag=rlk_av,limit=1] run function rlk:mboss/butterfly/fx/p/cure
execute unless entity @e[tag=rlk_av,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"ripple",pos:"~ ~0.07 ~",rot:"~ 90",bb:"fixed",roll:0,spin:50,s0:1.2,s1:5.2,move:"0f,0f,0f",life:8,fade:3,col:14736796}
function rlk:mboss/butterfly/fx/snd/cure_chime
