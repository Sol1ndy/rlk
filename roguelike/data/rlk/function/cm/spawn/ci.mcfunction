# 번개 시킨 (술사가 부름; 단독 소환은 시험용): transparent husk brain (pathing, health bar, hits) + display rig linked by cmId; at the caller's position
function rlk:cm/ci/lib/obj
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_newmob","rlk_cmb","rlk_cm_ci","rlk_m_cmci","rlk_cmnew","rlk_c2e","rlk_lobby"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,NoAI:1b,NoGravity:1b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],attributes:[{id:"minecraft:scale",base:0.5d},{id:"minecraft:movement_speed",base:0.0d}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
scoreboard players set @e[tag=rlk_cmnew] xpDrop 0
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/ci/init
