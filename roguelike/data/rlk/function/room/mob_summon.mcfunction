# 임시 몹 1마리 (위치 = 실행 위치). 55% 허스크 / 25% 스켈레톤 / 20% 변명자
execute store result score #r tmp run random value 1..100
execute if score #r tmp matches ..55 run summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_husk"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty"}
execute if score #r tmp matches 56..80 run summon minecraft:skeleton ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_skel"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",equipment:{mainhand:{id:"minecraft:bow",count:1},head:{id:"minecraft:leather_helmet",count:1,components:{"minecraft:unbreakable":{}}}},drop_chances:{mainhand:0.0f,head:0.0f}}
execute if score #r tmp matches 81.. run summon minecraft:vindicator ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_vind"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",equipment:{mainhand:{id:"minecraft:iron_axe",count:1,components:{"minecraft:attribute_modifiers":[]}}},drop_chances:{mainhand:0.0f}}
execute as @e[tag=rlk_newmob] run function rlk:room/mob_init
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.02 12
playsound minecraft:entity.zombie.infect master @a ~ ~ ~ 0.5 0.8
