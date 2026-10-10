# 챕터 테마 (맵을 만들 때): 1챕터 = 3 평원(몬드 · 리월), 2챕터 = 4 이나즈마(벚꽃 · 신사 · 궁전), 3챕터 = 5 수메르(구역마다 우림 / 사막), 4챕터 = 7 폰타인(강 · 호수 · 연못), 그 뒤 홀수 = 1 폐광산, 짝수 = 2 숲 (다른 챕터 테마는 차례로 바뀔 예정)
#   u = 아직 안 들어간 구역의 바닥(지도에서 구별됨) / v = 들어가 본 구역의 바닥 / w = 벽 / hb · tc · tc2 = 언덕 몸통 · 절벽 / pw · pb · pf = 낙사 구간 / st = 경사로 계단
scoreboard players set #th room 1
execute if score #chapter room matches 1.. run scoreboard players operation #th room = #chapter room
scoreboard players remove #th room 1
scoreboard players operation #th room %= #st2 tmp
scoreboard players add #th room 1
execute if score #chapter room matches ..1 run scoreboard players set #th room 3
execute if score #chapter room matches 2 run scoreboard players set #th room 4
execute if score #chapter room matches 3 run scoreboard players set #th room 5
execute if score #chapter room matches 4 run scoreboard players set #th room 7
execute if score #th room matches 1 run data modify storage rlk:room th set value {n:1,u:"minecraft:tuff",v:"minecraft:cobbled_deepslate",w:"minecraft:stone",hb:"minecraft:cobbled_deepslate",tc:"minecraft:stone",tc2:"minecraft:deepslate",pw:"minecraft:deepslate",pb:"minecraft:deepslate",pf:"minecraft:lava",st:"minecraft:cobblestone_stairs",lb:"minecraft:cobblestone",lb2:"minecraft:cobbled_deepslate"}
execute if score #th room matches 2 run data modify storage rlk:room th set value {n:2,u:"minecraft:podzol",v:"minecraft:grass_block",w:"minecraft:mossy_cobblestone",hb:"minecraft:dirt",tc:"minecraft:stone",tc2:"minecraft:mossy_cobblestone",pw:"minecraft:stone",pb:"minecraft:moss_block",pf:"minecraft:oak_leaves[persistent=true]",st:"minecraft:mossy_cobblestone_stairs",lb:"minecraft:mossy_cobblestone",lb2:"minecraft:cobblestone"}
execute if score #th room matches 3 run data modify storage rlk:room th set value {n:3,u:"minecraft:podzol",v:"minecraft:grass_block",w:"minecraft:stone",hb:"minecraft:dirt",tc:"minecraft:stone",tc2:"minecraft:andesite",pw:"minecraft:stone",pb:"minecraft:dirt",pf:"minecraft:azalea_leaves[persistent=true]",st:"minecraft:mossy_stone_brick_stairs",lb:"minecraft:stone_bricks",lb2:"minecraft:mossy_stone_bricks"}
execute if score #th room matches 4 run data modify storage rlk:room th set value {n:4,u:"minecraft:podzol",v:"minecraft:grass_block",w:"minecraft:stone",hb:"minecraft:dirt",tc:"minecraft:stone_bricks",tc2:"minecraft:mossy_stone_bricks",pw:"minecraft:stone",pb:"minecraft:dirt",pf:"minecraft:cherry_leaves[persistent=true]",st:"minecraft:stone_brick_stairs",lb:"minecraft:stone_bricks",lb2:"minecraft:cracked_stone_bricks"}
execute if score #th room matches 5 run data modify storage rlk:room th set value {n:5,u:"minecraft:podzol",v:"minecraft:grass_block",u2:"minecraft:red_sand",v2:"minecraft:sand",w:"minecraft:moss_block",hb:"minecraft:dirt",tc:"minecraft:mossy_cobblestone",tc2:"minecraft:stone",pw:"minecraft:stone",pb:"minecraft:dirt",pf:"minecraft:jungle_leaves[persistent=true]",st:"minecraft:mossy_cobblestone_stairs",lb:"minecraft:cut_sandstone",lb2:"minecraft:mud_bricks"}
execute if score #th room matches 7 run data modify storage rlk:room th set value {n:7,u:"minecraft:podzol",v:"minecraft:grass_block",w:"minecraft:stone",hb:"minecraft:dirt",tc:"minecraft:calcite",tc2:"minecraft:diorite",pw:"minecraft:stone",pb:"minecraft:clay",pf:"minecraft:water",st:"minecraft:stone_brick_stairs",lb:"minecraft:smooth_quartz",lb2:"minecraft:quartz_bricks"}
