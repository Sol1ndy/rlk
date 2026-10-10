# Only lock the camera after the player has actually reached the safe dome.
execute if entity @a[tag=player,scores={rdCam=1},limit=1] run return 0
execute unless entity @e[tag=rlk_rd_dome,limit=1] run return 0
scoreboard players set #rdSafe rd 0
execute as @e[tag=rlk_rd_dome,limit=1] at @s run function rlk:boss/raiden/dome_contains
execute if score #rdSafe rd matches 1 as @a[tag=player,limit=1] at @s run function rlk:boss/raiden/camera/start
