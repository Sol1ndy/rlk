# 1 when the executing floor point keeps her out of the player's camera line: her body (the point + 1 b) farther than
# 1.3 b from the player's eyes and from every point 0.5 .. 4 b behind them along their view.
# Round X (x_brief ruling 1): and off the player's BODY - the point at least 1.6 b from the avatar's feet (0.05 b of
# slack: a stop chosen at it passes). The eyes are the seat rider's, high over the avatar: the line alone passed with her on it.
execute if entity @e[tag=rlk_body,distance=..1.55] run return fail
summon minecraft:marker ~ ~1 ~ {Tags:["rlk_hr_camp","rlk_room","rlk_mb_aux"]}
scoreboard players set #sw_c hr 0
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-0 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-0.5 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-1 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-1.5 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-2 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-2.5 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-3 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-3.5 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^-4 if entity @e[type=minecraft:marker,tag=rlk_hr_camp,distance=..1.3] run scoreboard players set #sw_c hr 1
kill @e[type=minecraft:marker,tag=rlk_hr_camp]
execute if score #sw_c hr matches 1 run return fail
return 1
