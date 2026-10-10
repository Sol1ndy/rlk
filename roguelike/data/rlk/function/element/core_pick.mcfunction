# 풀 원핵이 떨어질 자리 (위치 = 몹 발): 무작위 방향으로 1.6~2.4칸, 벽 속이거나 다른 몹(1.1칸)과 겹치면 90도씩 돌려 다시(최대 4번). 결과 = rlk_cpos 표식(땅 위)
kill @e[tag=rlk_cpos]
kill @e[tag=rlk_cpo]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_cpo"]}
summon minecraft:marker ~ ~ ~ {Tags:["rlk_cpos"]}
execute store result entity @e[tag=rlk_cpo,limit=1] Rotation[0] float 1 run random value 0..359
scoreboard players set #cpOk tmp 0
function rlk:element/core_try
function rlk:element/core_try
function rlk:element/core_try
function rlk:element/core_try
# 땅에 내려놓기(최대 3칸)
execute as @e[tag=rlk_cpos] at @s if block ~ ~-0.05 ~ #rlk:dash_pass run tp @s ~ ~-0.5 ~
execute as @e[tag=rlk_cpos] at @s if block ~ ~-0.05 ~ #rlk:dash_pass run tp @s ~ ~-0.5 ~
execute as @e[tag=rlk_cpos] at @s if block ~ ~-0.05 ~ #rlk:dash_pass run tp @s ~ ~-0.5 ~
execute as @e[tag=rlk_cpos] at @s if block ~ ~-0.05 ~ #rlk:dash_pass run tp @s ~ ~-0.5 ~
execute as @e[tag=rlk_cpos] at @s if block ~ ~-0.05 ~ #rlk:dash_pass run tp @s ~ ~-0.5 ~
execute as @e[tag=rlk_cpos] at @s if block ~ ~-0.05 ~ #rlk:dash_pass run tp @s ~ ~-0.5 ~
kill @e[tag=rlk_cpo]
