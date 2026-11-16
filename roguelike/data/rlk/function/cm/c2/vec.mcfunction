# 실행 방향의 수평 단위 벡터 x1000 → #c2vx #c2vz (실행 위치 기준, 표식 rlk_c2vec 한 개를 옮겨 잼)
execute unless entity @e[tag=rlk_c2vec,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2vec","rlk_cmglob"]}
tp @e[tag=rlk_c2vec,limit=1] ^ ^ ^1
execute store result score #c2vx tmp run data get entity @e[tag=rlk_c2vec,limit=1] Pos[0] 1000
execute store result score #c2vz tmp run data get entity @e[tag=rlk_c2vec,limit=1] Pos[2] 1000
tp @e[tag=rlk_c2vec,limit=1] ~ ~ ~
execute store result score #c2t tmp run data get entity @e[tag=rlk_c2vec,limit=1] Pos[0] 1000
scoreboard players operation #c2vx tmp -= #c2t tmp
execute store result score #c2t tmp run data get entity @e[tag=rlk_c2vec,limit=1] Pos[2] 1000
scoreboard players operation #c2vz tmp -= #c2t tmp
