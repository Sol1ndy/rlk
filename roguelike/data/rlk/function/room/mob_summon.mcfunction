# 임시 몹 1마리 (위치 = 실행 위치). 55% 허스크 / 25% 스켈레톤 / 20% 변명자
# 1챕터: 커스텀 몹 6종(cm)
execute if score #chapter room matches ..1 run return run function rlk:cm/summon_c1
# 테스트 설정: 2챕터 이후에도 1챕터 커스텀 몹을 소환. 예전처럼 임시 몹을 쓰려면 /scoreboard players set #mobTmp room 1
execute if score #chapter room matches 2 unless score #mobTmp room matches 1 run return run function rlk:cm/c2/room_slot
execute unless score #mobTmp room matches 1 run return run function rlk:cm/summon_c1
execute store result score #r tmp run random value 1..100
execute if score #r tmp matches ..55 run summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_husk"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty"}
execute if score #r tmp matches 56..80 run summon minecraft:skeleton ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_skel"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",equipment:{mainhand:{id:"minecraft:bow",count:1},head:{id:"minecraft:leather_helmet",count:1,components:{"minecraft:unbreakable":{}}}},drop_chances:{mainhand:0.0f,head:0.0f}}
execute if score #r tmp matches 81.. run summon minecraft:vindicator ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_vind"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",equipment:{mainhand:{id:"minecraft:iron_axe",count:1,components:{"minecraft:attribute_modifiers":[]}}},drop_chances:{mainhand:0.0f}}
execute as @e[tag=rlk_newmob] run function rlk:room/mob_init
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.02 12
execute unless score #k0 snd matches 1 run function rlk:snd/f0
