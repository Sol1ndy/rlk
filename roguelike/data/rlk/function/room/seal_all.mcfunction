# 봉인 무늬 매 틱 (무늬가 있을 때만 호출). 가끔 문 앞에 붉은 불티
execute unless entity @e[tag=rlk_seal,limit=1] run return run scoreboard players set #seal room 0
execute as @e[tag=rlk_seal] run function rlk:room/seal_tick
scoreboard players add #sealP room 1
execute if score #sealP room matches 6.. run scoreboard players set #sealP room 0
execute if score #sealP room matches 0 as @e[tag=rlk_seal,scores={sidx=1,sph=1..2}] at @s run particle minecraft:dust{color:[1.0f,0.12f,0.1f],scale:0.7f} ~ ~1.5 ~ 0.9 0.9 0.9 0 2
