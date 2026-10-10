scoreboard players set #rdDrain rd 2
execute if score #elem tmp matches 3 run scoreboard players set #rdDrain rd 1
execute if score #elem tmp matches 1 run scoreboard players set #rdDrain rd 6
execute if score #elem tmp matches 4 run scoreboard players set #rdDrain rd 6
execute if score #elem tmp matches 7 run scoreboard players set #rdDrain rd 4
execute if score #elem tmp matches 2 run scoreboard players set #rdDrain rd 3
execute if score #elem tmp matches 5..6 run scoreboard players set #rdDrain rd 3
execute if score #tfm tmp matches 1 run scoreboard players set #rdDrain rd 1
scoreboard players operation @s rdShield -= #rdDrain rd
scoreboard players set @s rdHitCD 4
