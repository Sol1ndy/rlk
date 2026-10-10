# 방패병: 기존 1.25배 허스크 두뇌 + 독립적인 관절/방패 디스플레이
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_sh","rlk_m_cmsh","rlk_cmnew","rlk_cmbig"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],attributes:[{id:"minecraft:scale",base:1.25d}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/init
