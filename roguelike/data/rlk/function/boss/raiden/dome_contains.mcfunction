# The entire marked ground circle is safe, including a player jumping inside it.
execute unless entity @e[tag=rlk_body,distance=..7,limit=1] run return 0
execute store result score #rdSafeX rd run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result score #rdSafeZ rd run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
execute store result score #rdDomeX rd run data get entity @s Pos[0] 100
execute store result score #rdDomeZ rd run data get entity @s Pos[2] 100
scoreboard players operation #rdSafeX rd -= #rdDomeX rd
scoreboard players operation #rdSafeZ rd -= #rdDomeZ rd
scoreboard players operation #rdSafeX rd *= #rdSafeX rd
scoreboard players operation #rdSafeZ rd *= #rdSafeZ rd
scoreboard players operation #rdSafeX rd += #rdSafeZ rd
execute if score #rdSafeX rd matches ..160000 run scoreboard players set #rdSafe rd 1
