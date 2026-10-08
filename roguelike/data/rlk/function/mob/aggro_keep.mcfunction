# @s = 몹 (0.5초마다). 공격 대상이 없으면 몸을 다시 노리게 한다
execute if score @s stunT matches 1.. run return 0
execute if score @s frzT matches 1.. run return 0
execute if entity @s[tag=rlk_agq] run return 0
scoreboard players set #hasT tmp 0
execute on target run scoreboard players set #hasT tmp 1
execute if score #hasT tmp matches 1 run return 0
execute if data entity @s {NoAI:1b} run return 0
damage @s 0 minecraft:generic by @e[tag=rlk_body,limit=1]
