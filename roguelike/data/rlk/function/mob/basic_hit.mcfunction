# @s = 기본 공격에 맞은 몹, at @s. 보스는 경직·넉백 없음
execute if entity @s[tag=boss] run return 0
scoreboard players operation @s stunT = #stunBasic tmp
execute unless entity @s[tag=boss] if entity @e[tag=rlk_body,limit=1] run function rlk:mob/knock
