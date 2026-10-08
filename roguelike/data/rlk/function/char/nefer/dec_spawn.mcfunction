# 기만의 핵 (위치 = 생길 자리): 폭발하지 않고 만개·발화도 안 됨. 15초 뒤 사라짐. 환영극이 흡수한다
kill @e[tag=rlk_cpos]
summon minecraft:marker ~ ~0.5 ~ {Tags:["rlk_cpos"]}
execute as @e[tag=rlk_cpos] run spreadplayers ~ ~ 0 1.2 false @s
execute at @e[tag=rlk_cpos,limit=1] run function rlk:char/nefer/dec_model
kill @e[tag=rlk_cpos]
scoreboard players operation @e[tag=rlk_dc_new] life = #nfDecDur tmp
tag @e[tag=rlk_dc_new] remove rlk_dc_new
playsound minecraft:block.sculk_sensor.clicking master @a ~ ~ ~ 0.6 1.4
execute store result score #cc tmp if entity @e[tag=rlk_dcore]
execute if score #cc tmp matches 6.. run kill @e[tag=rlk_dcore,limit=1]
