# 파편 하나 (위치 = 반응이 일어난 몹). 무작위 방향으로 튀어 나간다. 맞힐 몹 번호 #shTg
summon minecraft:block_display ~ ~1.2 ~ {Tags:["rlk_rnsh","rlk_rnsh_new"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:packed_ice"},transformation:{translation:[-0.06f,-0.06f,-0.3f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.12f,0.12f,0.6f]}}
execute store result entity @e[tag=rlk_rnsh_new,limit=1] Rotation[0] float 1 run random value -180..179
execute store result entity @e[tag=rlk_rnsh_new,limit=1] Rotation[1] float 1 run random value -55..-15
scoreboard players operation @e[tag=rlk_rnsh_new] rnTg = #shTg tmp
scoreboard players operation @e[tag=rlk_rnsh_new] rxDmg = #qDmg tmp
scoreboard players set @e[tag=rlk_rnsh_new] life 0
tag @e[tag=rlk_rnsh_new] remove rlk_rnsh_new
scoreboard players add #shN tmp 1
