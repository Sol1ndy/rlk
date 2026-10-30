# Pull the player's body to the execution position over t ticks (t 0 = at once), as anything, positioned at
# the destination (e.g. 1.2 b in front of the boss). Dash i-frames do not stop it; dead / revival / selection
# screen / map view / a dying boss refuse it (returns fail). Option #pullFace mb 1 (default): turn the player to
# the boss.
scoreboard players operation #plFace mb = #pullFace mb
scoreboard players set #pullFace mb 1
execute if score #mbSt mb matches 2 run return fail
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return fail
execute if entity @a[tag=player,scores={rnDie=1..}] run return fail
execute if entity @a[tag=player,scores={pkMode=1..}] run return fail
execute if entity @a[tag=player,scores={vMap=1}] run return fail
kill @e[tag=rlk_mb_pullpt]
kill @e[tag=rlk_plkb]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_pullpt","rlk_mb_aux","rlk_room"]}
scoreboard players set #mbPlOn mb 1
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_pullpt,limit=1] mbPlT $(t)
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_pullpt,limit=1] mbPlF = #plFace mb
execute as @a[tag=player,limit=1] run scoreboard players set @s stepT 0
execute if entity @e[tag=rlk_av,limit=1] as @a[tag=player,limit=1] run function rlk:view/stop_h
execute as @e[tag=rlk_mb_pullpt,limit=1] if score @s mbPlT matches ..0 at @s run function rlk:mboss/pull/finish
return 1
