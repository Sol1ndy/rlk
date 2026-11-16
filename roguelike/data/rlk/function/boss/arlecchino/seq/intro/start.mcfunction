# Intro (PLAN §3.1: tea, cup to embers, wisps flee, reach, crimson vortex, the scythe forms, hold + title, the 360 twirl, flip, stance, push ring). @s = the body, at it; #sq kn = 0. Plays the rig clip intro (150 t).
scoreboard players set #sqdone kn 0
function rlk:boss/arlecchino/rig/play/intro
kill @e[type=marker,tag=rlk_kn_wisp]
summon minecraft:marker ~1.3 ~0.6 ~0 {Tags:["rlk_room","rlk_mb_aux","rlk_kn_prop","rlk_kn_wisp","rlk_kn_wisp_0"]}
execute as @e[type=marker,tag=rlk_kn_wisp_0,limit=1] at @s run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
summon minecraft:marker ~-0.65 ~0.86 ~1.13 {Tags:["rlk_room","rlk_mb_aux","rlk_kn_prop","rlk_kn_wisp","rlk_kn_wisp_1"]}
execute as @e[type=marker,tag=rlk_kn_wisp_1,limit=1] at @s run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
summon minecraft:marker ~-0.65 ~0.34 ~-1.13 {Tags:["rlk_room","rlk_mb_aux","rlk_kn_prop","rlk_kn_wisp","rlk_kn_wisp_2"]}
execute as @e[type=marker,tag=rlk_kn_wisp_2,limit=1] at @s run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
function rlk:boss/arlecchino/rig/look/props/tea
