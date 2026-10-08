# 활 매 틱 (@s = 플레이어, at 몸)
execute if score @s bowCd matches 1.. run scoreboard players remove @s bowCd 1
function rlk:char/bow/queue_tick
execute if score @s bowT matches 1.. run function rlk:char/bow/charge_tick
scoreboard players set #bowChg tmp 0
