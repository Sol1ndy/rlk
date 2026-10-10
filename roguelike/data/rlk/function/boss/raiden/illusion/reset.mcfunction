execute as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/vanish
kill @e[type=minecraft:item_display,tag=rlk_rd_ilvis]
execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run function rlk:boss/raiden/hazard/expire
tag @e[tag=rlk_rd_ilhaz] remove rlk_rd_ilhaz
tag @e[tag=rlk_rd_ilact] remove rlk_rd_ilact
scoreboard players set #rdIlStep rd 0
scoreboard players set #rdIlClock rd 0
scoreboard players set #rdIlTurn rd 0
scoreboard players set #rdIlSlash rd 0
scoreboard players set #rdIlShots rd 0
