function rlk:cm/cn/can_spawn
execute unless score #cnSpawnOk tmp matches 1 run return 0
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_cn","rlk_m_cmcn","rlk_cmnew"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,NoAI:1b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/init
return 1
