# 원시 정령 기계·재구성자: transparent husk brain (pathing, health bar, hits) + display rig linked by cmId; at the caller's position
function rlk:cm/pc/lib/obj
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_pc","rlk_m_cmpc","rlk_cmnew","rlk_c3e"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],attributes:[{id:"minecraft:scale",base:1.15d},{id:"minecraft:movement_speed",base:0.22d}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
scoreboard players set @e[tag=rlk_cmnew] xpDrop 14
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/pc/init
