# 개화: 풀 씨앗 생성(6초 뒤 폭발, 최대 5개 — 넘치면 가장 오래된 것이 바로 폭발)
execute if score #nfDecT tmp matches 1.. run return run function rlk:char/nefer/dec_spawn
# 자리(주변 1.2칸 땅 위)를 먼저 고르고 그 자리에 모델을 놓는다
kill @e[tag=rlk_cpos]
summon minecraft:marker ~ ~0.5 ~ {Tags:["rlk_cpos"]}
execute as @e[tag=rlk_cpos] run spreadplayers ~ ~ 0 1.2 false @s
execute at @e[tag=rlk_cpos,limit=1] run function rlk:element/core_model
kill @e[tag=rlk_cpos]
scoreboard players set @e[tag=rlk_core_new] life 120
scoreboard players set @e[tag=rlk_core_new] rxQ 0
scoreboard players operation @e[tag=rlk_core_new] rxDmg = #qDmg tmp
scoreboard players operation @e[tag=rlk_core_new] rxDmg3 = #qDmg3 tmp
tag @e[tag=rlk_core_new] remove rlk_core_new
playsound minecraft:block.moss.place master @a ~ ~ ~ 0.8 1.3
execute store result score #cc tmp if entity @e[tag=rlk_core]
execute if score #cc tmp matches 6.. run scoreboard players set @e[tag=rlk_core,limit=1] life 0
