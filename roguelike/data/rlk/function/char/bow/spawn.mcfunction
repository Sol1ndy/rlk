# 화살 생성 (위치·방향 = 실행 위치·방향). 입력: #aKind(1 기본 / 2 조준 / 3 풀차지 / 4 염초 화살(추적) / 5 기본(염초 정화) / 6 유금 운간초)
#   #aEl(원소) #aSub(틱당 0.5칸 이동 횟수) #aLife(수명 틱) #aIcd(1 = 부착 쿨 적용) + #dmg #crit. 만든 화살에는 rlk_arrnew 태그가 남아 있다(부른 쪽이 방향을 고친 뒤 뗀다)
execute if score #aKind tmp matches 1..2 if score #aEl tmp matches 0 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:stripped_birch_log"},transformation:{translation:[-0.03f,-0.03f,-0.9f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.06f,0.06f,0.9f]}}
execute if score #aKind tmp matches 1..2 unless score #aEl tmp matches 0 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:glowstone"},transformation:{translation:[-0.035f,-0.035f,-0.9f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.07f,0.07f,0.9f]}}
execute if score #aKind tmp matches 3 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:shroomlight"},transformation:{translation:[-0.045f,-0.045f,-1.1f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.09f,0.09f,1.1f]}}
execute if score #aKind tmp matches 4 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:shroomlight"},transformation:{translation:[-0.035f,-0.035f,-0.5f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.07f,0.07f,0.5f]}}
execute if score #aKind tmp matches 5 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:shroomlight"},transformation:{translation:[-0.035f,-0.035f,-0.9f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.07f,0.07f,0.9f]}}
execute if score #aKind tmp matches 6 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:magma_block"},transformation:{translation:[-0.11f,-0.11f,-1.3f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.22f,0.22f,1.3f]}}
tp @e[tag=rlk_arrnew] ~ ~ ~ ~ ~
scoreboard players operation @e[tag=rlk_arrnew] jdmg = #dmg tmp
scoreboard players operation @e[tag=rlk_arrnew] jcrit = #crit tmp
scoreboard players operation @e[tag=rlk_arrnew] aKind = #aKind tmp
scoreboard players operation @e[tag=rlk_arrnew] aEl = #aEl tmp
scoreboard players operation @e[tag=rlk_arrnew] aSub = #aSub tmp
scoreboard players operation @e[tag=rlk_arrnew] aLife = #aLife tmp
scoreboard players operation @e[tag=rlk_arrnew] aIcd = #aIcd tmp
scoreboard players set @e[tag=rlk_arrnew] life 0
