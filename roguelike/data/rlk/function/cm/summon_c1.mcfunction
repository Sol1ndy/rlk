# 1챕터 몹 1마리. 대포병 후보가 좁으면 주변 평지를 찾고, 없으면 일반 몹으로 재추첨한다.
execute store result score #cmRoll tmp run random value 1..100
execute if score #cmRoll tmp matches 87.. run function rlk:cm/spawn_cn_nearby
execute if score #cmRoll tmp matches 87.. if score #cnSpawnOk tmp matches 0 store result score #cmRoll tmp run random value 1..86
execute if score #cmRoll tmp matches ..30 run function rlk:cm/spawn/sw
execute if score #cmRoll tmp matches 31..48 run function rlk:cm/spawn/ar
execute if score #cmRoll tmp matches 49..60 run function rlk:cm/spawn/fm
execute if score #cmRoll tmp matches 61..72 run function rlk:cm/spawn/im
execute if score #cmRoll tmp matches 73..86 run function rlk:cm/spawn/sh
execute as @e[tag=rlk_newmob] run function rlk:room/mob_init
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.02 12
execute unless score #k0 snd matches 1 run function rlk:snd/f0
