# 개화: 풀 씨앗 생성(6초 뒤 폭발, 최대 5개 — 넘치면 가장 오래된 것이 바로 폭발)
execute if score #nfDecT tmp matches 1.. run return run function rlk:char/nefer/dec_spawn
# 떨어질 자리(몹 주변, 겹치지 않게)를 고르고, 몹 가운데에서 생겨 포물선을 그리며 날아간다
function rlk:element/core_pick
execute positioned ~ ~1 ~ run function rlk:element/core_model
execute as @e[tag=rlk_core_new] run function rlk:element/core_fly_init
kill @e[tag=rlk_cpos]
scoreboard players set @e[tag=rlk_core_new] life 120
scoreboard players set @e[tag=rlk_core_new] rxQ 0
scoreboard players operation @e[tag=rlk_core_new] rxDmg = #qDmg tmp
scoreboard players operation @e[tag=rlk_core_new] rxDmg3 = #qDmg3 tmp
tag @e[tag=rlk_core_new] remove rlk_core_new
execute unless score #k67 snd matches 1 run function rlk:snd/f70
execute store result score #cc tmp if entity @e[tag=rlk_core]
execute if score #cc tmp matches 6.. run scoreboard players set @e[tag=rlk_core,limit=1] life 0
