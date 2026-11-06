# 우인단 번개 시킨 술사: transparent husk brain (pathing, health bar, hits) + display rig linked by cmId; at the caller's position
function rlk:cm/cc/lib/obj
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_cc","rlk_m_cmcc","rlk_cmnew","rlk_c2e"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],attributes:[{id:"minecraft:scale",base:1.0d},{id:"minecraft:movement_speed",base:0.24d}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
scoreboard players set @e[tag=rlk_cmnew] xpDrop 10
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/cc/init
