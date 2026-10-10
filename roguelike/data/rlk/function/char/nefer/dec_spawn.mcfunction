# 기만의 핵 (위치 = 생길 자리): 폭발하지 않고 만개·발화도 안 됨. 15초 뒤 사라짐. 환영극이 흡수한다
execute if score #cpHere tmp matches 1 positioned ~ ~0.5 ~ run function rlk:char/nefer/dec_model
execute unless score #cpHere tmp matches 1 run function rlk:element/core_pick
execute unless score #cpHere tmp matches 1 positioned ~ ~1 ~ run function rlk:char/nefer/dec_model
execute unless score #cpHere tmp matches 1 as @e[tag=rlk_dc_new] run function rlk:element/core_fly_init
kill @e[tag=rlk_cpos]
scoreboard players operation @e[tag=rlk_dc_new] life = #nfDecDur tmp
tag @e[tag=rlk_dc_new] remove rlk_dc_new
execute unless score #k328 snd matches 1 run function rlk:snd/f384
execute store result score #cc tmp if entity @e[tag=rlk_dcore]
execute if score #cc tmp matches 6.. run kill @e[tag=rlk_dcore,limit=1]
