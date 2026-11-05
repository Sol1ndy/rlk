# The seat rock again (the intro replay).
kill @e[tag=rlk_hr_deco_seat_rock]
summon minecraft:item_display 884.0 201 5.0 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_deco","rlk_hr_deco_seat_rock","rlk_hr_dnew"]}
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ 187.31 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run function rlk:boss/scarlet/fx/prop/seat_rock {look:"bottle"}
tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew
