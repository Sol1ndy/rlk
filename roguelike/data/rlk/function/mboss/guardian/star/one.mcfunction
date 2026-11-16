# @s = star husk, at @s: permanent aura of an active star ("기록 원소 상시 부착"), sparks, break check.
scoreboard players add @s mbT 1
execute if score @s mbS matches 1 run scoreboard players set @s aFire 1000
execute if score @s mbS matches 2 run scoreboard players set @s aWater 1000
execute if score @s mbS matches 3 run scoreboard players set @s aThunder 1000
execute if score @s mbS matches 4 run scoreboard players set @s aIce 1000
execute if score @s mbS matches 1..4 run scoreboard players set @s elAct 1
scoreboard players operation #gdM mb = @s mbT
scoreboard players operation #gdM mb %= #gdK4 mb
execute if score #gdM mb matches 0 if score @s mbS matches 1 run particle minecraft:flame ~ ~1.3 ~ 0.35 0.45 0.35 0.02 2 force @a[tag=player]
execute if score #gdM mb matches 0 if score @s mbS matches 2 run particle minecraft:falling_water ~ ~1.3 ~ 0.35 0.45 0.35 0 2 force @a[tag=player]
execute if score #gdM mb matches 0 if score @s mbS matches 3 run particle minecraft:electric_spark ~ ~1.3 ~ 0.35 0.45 0.35 0.05 2 force @a[tag=player]
execute if score #gdM mb matches 0 if score @s mbS matches 4 run particle minecraft:snowflake ~ ~1.3 ~ 0.35 0.45 0.35 0.02 2 force @a[tag=player]
execute if score #gdM mb matches 0 if score @s mbS matches 5 run particle minecraft:wax_on ~ ~1.3 ~ 0.35 0.45 0.35 0 2 force @a[tag=player]
execute if score #gdM mb matches 0 if score @s mbS matches 6 run particle minecraft:end_rod ~ ~1.3 ~ 0.35 0.45 0.35 0.01 2 force @a[tag=player]
execute if entity @s[tag=rlk_mb_broken] run function rlk:mboss/guardian/star/broke
