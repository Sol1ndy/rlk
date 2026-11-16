# 그림자 닌자: transparent husk brain (pathing, health bar, hits) + display rig linked by cmId; at the caller's position
function rlk:cm/nj/lib/obj
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_nj","rlk_m_cmnj","rlk_cmnew","rlk_c2e"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],attributes:[{id:"minecraft:scale",base:0.96d},{id:"minecraft:movement_speed",base:0.38d}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
scoreboard players set @e[tag=rlk_cmnew] xpDrop 9
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/nj/init
