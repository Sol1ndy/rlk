# Spear 1: lock the player's position, the hazard (element/colour by the star kind) and the giant
# red spear hanging point-down, its tip 3.8 b above the target (prop scale 5.5: tip 8.1 b below the grip).
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13t0"]}
scoreboard players set #hzSfx mb 4
scoreboard players set #hzKB mb 3
execute if score #gdFailK1 mb matches 1 run scoreboard players set #hzEl mb 1
execute if score #gdFailK1 mb matches 1 run scoreboard players set #hzCol mb 1
execute if score #gdFailK1 mb matches 2 run scoreboard players set #hzEl mb 2
execute if score #gdFailK1 mb matches 2 run scoreboard players set #hzCol mb 2
execute if score #gdFailK1 mb matches 3 run scoreboard players set #hzEl mb 3
execute if score #gdFailK1 mb matches 3 run scoreboard players set #hzCol mb 3
execute if score #gdFailK1 mb matches 4 run scoreboard players set #hzEl mb 4
execute if score #gdFailK1 mb matches 4 run scoreboard players set #hzCol mb 4
execute if score #gdFailK1 mb matches 5 run scoreboard players set #hzCol mb 5
execute if score #gdFailK1 mb matches 6 run scoreboard players set #hzCol mb 2
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] run function rlk:mboss/hz/disc {r:28,tell:24,dmg:220}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] positioned ~ ~11.9 ~ rotated 0 0 run function rlk:mboss/guardian/rig/prop/spear
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] {transformation:{left_rotation:[1f,0f,0f,0f],scale:[5.5f,5.5f,5.5f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/guardian/prop_spear_red"}}}
tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p13s0
tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p13
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~11 ~ 0.3 1.2 0.3 0 20 force @a[tag=player]
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.3
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.3
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.3
function rlk:mboss/guardian/voice/attack
