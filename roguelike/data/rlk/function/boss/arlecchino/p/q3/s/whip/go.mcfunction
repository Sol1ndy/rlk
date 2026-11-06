# Q3 stage whip: tick 0 (@s = body), clip q3.
scoreboard players set #q3_s kn 1
scoreboard players set #q3_c kn 0
function rlk:boss/arlecchino/rig/play/q3
execute at @s run function rlk:boss/arlecchino/fx/snd/rear_whip
function rlk:boss/arlecchino/rig/anchor/spine
execute if entity @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] at @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] rotated as @s rotated ~ 0 run function rlk:boss/arlecchino/fx/p/legs_burst
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] at @s rotated as @s rotated ~ 0 positioned ~ ~1.6 ~ run function rlk:boss/arlecchino/fx/p/legs_burst
