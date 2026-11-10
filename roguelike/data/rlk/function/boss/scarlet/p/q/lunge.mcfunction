# Q ghost lunge (@s = the body, tick 16): along the locked aim to within 2 b of the locked spot, at most 14 b
# (0.5 b probe steps through mv/ok), in 4 t.
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
execute at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_dp"]}
execute at @s rotated as @s as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #t hr 28
scoreboard players set #t2 hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] at @s run function rlk:boss/scarlet/p/q/lstep
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] run function rlk:mboss/mv/glide {t:4}
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
