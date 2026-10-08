# 챕터 테마 (맵을 만들 때): 홀수 챕터 = 1 폐광산, 짝수 챕터 = 2 숲. rlk:room th = 블록 묶음
#   u = 아직 안 들어간 구역의 바닥(지도에서 구별됨) / v = 들어가 본 구역의 바닥 / w = 벽 / pw·pb·pf = 낙사 구간의 벽·바닥·바닥을 덮는 블록(몹 길찾기가 피하는 것)
scoreboard players set #th room 1
execute if score #chapter room matches 1.. run scoreboard players operation #th room = #chapter room
scoreboard players remove #th room 1
scoreboard players operation #th room %= #st2 tmp
scoreboard players add #th room 1
execute if score #th room matches 1 run data modify storage rlk:room th set value {n:1,u:"minecraft:tuff",v:"minecraft:cobbled_deepslate",w:"minecraft:stone",pw:"minecraft:deepslate",pb:"minecraft:deepslate",pf:"minecraft:lava"}
execute if score #th room matches 2 run data modify storage rlk:room th set value {n:2,u:"minecraft:podzol",v:"minecraft:grass_block",w:"minecraft:mossy_cobblestone",pw:"minecraft:stone",pb:"minecraft:moss_block",pf:"minecraft:oak_leaves[persistent=true]"}
