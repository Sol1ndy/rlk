# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# @s = a wall lock (the player's feet and facing at the cast start), at it, rotated as it: a new wall group (marker
# rlk_mb_ap_wall, its clock and id) and, by the lock's variant: 0 = three groups 120 deg apart at r 4.2 round the feet,
# 1 = one arc at r 3.6 ahead; each group 3 blades over a 60 deg arc and barrier blocks along the arc (y 201-202).
scoreboard players add #apWid mb 1
summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_wall","rlk_mb_ap_new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_ap_new] apL = #apWid mb
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apT 0
tag @e[type=minecraft:marker,tag=rlk_mb_ap_new] remove rlk_mb_ap_new
execute if score @s apS matches 1 run function rlk:boss/apep/wall/arc1
execute unless score @s apS matches 1 run function rlk:boss/apep/wall/arc3
execute at @s run function rlk:boss/apep/fx/snd/o4_rise
kill @s
