# 구역에 처음 들어옴 (@s = 구역 표식, at @s). 이때 비로소 적/보상이 나타난다
scoreboard players set @s zst 2
function rlk:room/cells_kill
function rlk:room/wave_start
execute if score @s zkind matches 1 run return run function rlk:room/combat_start
execute if score @s zkind matches 9 run return run function rlk:room/combat_start
scoreboard players set @s zst 3
execute if score @s zkind matches 2 run function rlk:room/end_setup
execute if score @s zkind matches 3 run function rlk:room/obj/k_money
execute if score @s zkind matches 4 run function rlk:room/obj/k_shop
execute if score @s zkind matches 5 run function rlk:room/obj/k_sapphire
execute if score @s zkind matches 6 run function rlk:room/obj/k_reforge
execute if score @s zkind matches 7 run function rlk:room/obj/k_enchant
playsound minecraft:block.amethyst_block.chime master @a ~ ~ ~ 1 0.9
