execute as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/vanish
kill @e[type=minecraft:item_display,tag=rlk_rd_ilvis]
kill @e[tag=rlk_rd_ilspot]
execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run function rlk:boss/raiden/hazard/expire
tag @e[tag=rlk_rd_ilhaz] remove rlk_rd_ilhaz
scoreboard players set #rdIlStep rd 0
