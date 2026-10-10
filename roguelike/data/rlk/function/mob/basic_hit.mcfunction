# @s = 기본 공격에 맞은 몹, at @s. 보스는 경직·넉백 없음
execute if entity @s[tag=boss] run return 0
execute if entity @s[tag=rlk_cm_cn] run return 0
# 커스텀 몹 차지 중: 경직 없이 밀려나기만
execute if entity @s[tag=rlk_cmch] if entity @e[tag=rlk_body,limit=1] run return run function rlk:mob/knock
scoreboard players operation @s stunT = #stunBasic tmp
execute unless entity @s[tag=boss] if entity @e[tag=rlk_body,limit=1] run function rlk:mob/knock
