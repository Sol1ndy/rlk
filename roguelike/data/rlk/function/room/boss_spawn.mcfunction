# 임시 보스 (@s = 보스 구역 표식, at @s): 커다란 허스크
summon minecraft:husk ~ ~ ~ {PersistenceRequired:1b,DeathLootTable:"minecraft:empty",CustomName:{text:"수문장",color:"#E06A5A",bold:true},Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_boss","boss"]}
execute as @e[tag=rlk_newmob] run attribute @s minecraft:scale base set 2.2
execute as @e[tag=rlk_newmob] run attribute @s minecraft:movement_speed base set 0.27
execute as @e[tag=rlk_newmob] run function rlk:room/mob_init
particle minecraft:large_smoke ~ ~1.5 ~ 0.8 1.2 0.8 0.02 60
playsound minecraft:entity.wither.spawn master @a ~ ~ ~ 0.5 0.8
