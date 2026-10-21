# Ribbons every 2 t at each orb, the loop at the orb nearest the player every 20 t.
scoreboard players operation #azM mb = #azBgLT mb
scoreboard players operation #azM mb %= #azK4 mb
execute if score #azM mb matches 0 run execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d0,limit=1] at @s run function rlk:mboss/azhdaha/p/orbs/rib
scoreboard players operation #azM mb = #azBgLT mb
scoreboard players operation #azM mb %= #azK4 mb
execute if score #azM mb matches 1 run execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d1,limit=1] at @s run function rlk:mboss/azhdaha/p/orbs/rib
scoreboard players operation #azM mb = #azBgLT mb
scoreboard players operation #azM mb %= #azK4 mb
execute if score #azM mb matches 2 run execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d2,limit=1] at @s run function rlk:mboss/azhdaha/p/orbs/rib
scoreboard players operation #azM mb = #azBgLT mb
scoreboard players operation #azM mb %= #azK4 mb
execute if score #azM mb matches 3 run execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d3,limit=1] at @s run function rlk:mboss/azhdaha/p/orbs/rib
scoreboard players operation #azM mb = #azBgLT mb
scoreboard players operation #azM mb %= #azK20 mb
execute if score #azM mb matches 5 run execute at @e[tag=rlk_body,limit=1] at @e[type=minecraft:item_display,tag=rlk_mb_az_p31d,sort=nearest,limit=1] run function rlk:mboss/azhdaha/fx/snd/orb_loop
