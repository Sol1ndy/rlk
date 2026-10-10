# 재가 된 만상에 맞은 적 (@s = 몹, at @s): #arSkStun 틱 경직 + 몸에서 먼 쪽으로 #arSkKb 넉백, 위로 살짝
execute if entity @s[tag=rlk_cm_cn] run return 0
execute unless entity @s[tag=rlk_cmch] run function rlk:mob/stun
execute unless entity @s[tag=rlk_cmch] run scoreboard players operation @s stunT = #arSkStun tmp
execute unless entity @s[tag=rlk_cmch] run effect give @s minecraft:slowness 1 250 true
scoreboard players operation #kbSave tmp = #kbBasic tmp
scoreboard players operation #kbBasic tmp = #arSkKb tmp
function rlk:mob/knock
scoreboard players operation #kbBasic tmp = #kbSave tmp
data modify entity @s Motion[1] set value 0.22d
