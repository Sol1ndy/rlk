# 성수 전갈: transparent husk brain (pathing, health bar, hits) + display rig linked by cmId; at the caller's position
function rlk:cm/cs/lib/obj
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_cs","rlk_m_cmcs","rlk_cmnew","rlk_c3e"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],attributes:[{id:"minecraft:scale",base:1.1d},{id:"minecraft:movement_speed",base:0.27d}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
scoreboard players set @e[tag=rlk_cmnew] xpDrop 14
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/cs/init
