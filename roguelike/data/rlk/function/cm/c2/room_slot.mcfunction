# 2챕터 방 몹: 계획(rlk:c2 plan)의 맨 앞 무리를 실행 위치에 (room/mob_summon 에서). 몸 쪽을 보고 선다
execute unless data storage rlk:c2 plan[0] run data modify storage rlk:c2 plan append value {id:"g_ns",n:4}
data modify storage rlk:c2 cur set from storage rlk:c2 plan[0]
data remove storage rlk:c2 plan[0]
execute store result score #c2Size tmp run data get storage rlk:c2 cur.n
scoreboard players set #c2SizeSet tmp 1
execute if entity @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/spawn_id with storage rlk:c2 cur
execute unless entity @e[tag=rlk_body,limit=1] run function rlk:cm/c2/spawn_id with storage rlk:c2 cur
scoreboard players set #c2SizeSet tmp 0
execute as @e[tag=rlk_newmob] run function rlk:room/mob_init
particle minecraft:poof ~ ~1 ~ 0.6 0.6 0.6 0.02 16
execute unless score #c2arrive snd matches 1 run function rlk:cm/c2/snd/arrive
