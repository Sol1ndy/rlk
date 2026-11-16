# One drain per 5 ticks however many hits/DoT ticks land. #elem: 0 physical 1 fire 2 water
# 3 thunder 4 ice 5 rock 6 wind 7 grass 8 void; reaction/DoT damage (#tfm) drains least.
scoreboard players set #rdDrain rd 2
execute if score #elem tmp matches 1 run scoreboard players set #rdDrain rd 6
execute if score #elem tmp matches 4 run scoreboard players set #rdDrain rd 6
execute if score #elem tmp matches 2 run scoreboard players set #rdDrain rd 3
execute if score #elem tmp matches 5 run scoreboard players set #rdDrain rd 3
execute if score #elem tmp matches 6 run scoreboard players set #rdDrain rd 3
execute if score #elem tmp matches 7 run scoreboard players set #rdDrain rd 4
execute if score #tfm tmp matches 1 run scoreboard players set #rdDrain rd 1
scoreboard players operation @s rdShield -= #rdDrain rd
scoreboard players set @s rdHitCD 5
