# @s = pull point, at @s. Glide: body += (point - body) / ticks left, collision-checked like knockback.
scoreboard players set #mbPlOn mb 1
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run kill @s
execute if entity @a[tag=player,scores={rnDie=1..}] run return run kill @s
execute if entity @a[tag=player,scores={pkMode=1..}] run return run kill @s
execute if entity @a[tag=player,scores={vMap=1}] run return run kill @s
execute unless entity @e[tag=rlk_body,limit=1] run return run kill @s
execute if score @s mbPlT matches ..1 run return run function rlk:mboss/pull/finish
execute store result score #bx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #by mb run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000
execute store result score #bz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute store result score #px mb run data get entity @s Pos[0] 1000
execute store result score #py mb run data get entity @s Pos[1] 1000
execute store result score #pz mb run data get entity @s Pos[2] 1000
scoreboard players operation #px mb -= #bx mb
scoreboard players operation #px mb /= @s mbPlT
scoreboard players operation #px mb += #bx mb
scoreboard players operation #py mb -= #by mb
scoreboard players operation #py mb /= @s mbPlT
scoreboard players operation #py mb += #by mb
scoreboard players operation #pz mb -= #bz mb
scoreboard players operation #pz mb /= @s mbPlT
scoreboard players operation #pz mb += #bz mb
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[0] double 0.001 run scoreboard players get #px mb
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[1] double 0.001 run scoreboard players get #py mb
execute store result entity @e[tag=rlk_mb_help,limit=1] Pos[2] double 0.001 run scoreboard players get #pz mb
scoreboard players set #pkbBlocked tmp 0
execute at @e[tag=rlk_mb_help,limit=1] run function rlk:player/knockback/check
execute if score #pkbBlocked tmp matches 0 at @e[tag=rlk_mb_help,limit=1] run tp @e[tag=rlk_body,limit=1] ~ ~ ~
kill @e[tag=rlk_mb_help]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:reverse_portal ~ ~1 ~ 0.2 0.4 0.2 0.05 4 force @a[tag=player]
scoreboard players remove @s mbPlT 1
