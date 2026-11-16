# MX retreat (@s = the body, tick 0; the player nearer than 6 b): a 12-t leap straight back to about 9 b
# from them (probed through mv/ok), the backstep clip; the pattern clock waits (#mx_pre).
scoreboard players set #mx_pre hr 12
function rlk:boss/scarlet/rig/play/backstep
function rlk:mboss/mv/dist
scoreboard players set #t hr 90
scoreboard players operation #t hr -= #mbDist mb
scoreboard players operation #t hr /= #c5 hr
execute if score #t hr matches ..0 run scoreboard players set #t hr 1
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run function rlk:boss/scarlet/core/dash/probe
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] run function rlk:mboss/mv/leap {t:12,h:10}
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
execute at @s run function rlk:boss/scarlet/fx/snd/g_leap
