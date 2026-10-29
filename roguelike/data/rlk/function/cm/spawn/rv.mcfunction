# 성수 붉은 독수리: transparent husk brain (pathing, health bar, hits) + display rig linked by cmId; at the caller's position
function rlk:cm/rv/lib/obj
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_rv","rlk_m_cmrv","rlk_cmnew","rlk_c3e"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,NoAI:1b,NoGravity:1b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],attributes:[{id:"minecraft:scale",base:0.9d},{id:"minecraft:movement_speed",base:0.0d}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
scoreboard players set @e[tag=rlk_cmnew] xpDrop 12
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/rv/init
