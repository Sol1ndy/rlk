# The decor props at spawn (PLAN §6.7): the moon halo (p1), 8 lotus buds, the seat rock (bottle).
kill @e[type=minecraft:item_display,tag=rlk_hr_deco]
summon minecraft:item_display 889 218 -33 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_moon_halo","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 12.38 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/moon_halo {look:"p1"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 859.5 200.9 -13.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 0 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 864.5 200.9 -19.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 47 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 871.5 200.9 -20.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 94 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 877.5 200.9 -23.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 141 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 884.5 200.9 -21.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 188 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 899.5 200.9 -14.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 235 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 903.5 200.9 -14.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 282 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 890.5 200.9 -19.5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_lotus","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 329 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/lotus {look:"bud"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
summon minecraft:item_display 884 201 5 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_seat_rock","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 187.31 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/seat_rock {look:"bottle"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
