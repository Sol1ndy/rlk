# @s = 플레이어, at @s. 봉인된 검 1개 → 마검 키리온 + 카운터 리셋 + 이펙트
function rlk:items/order_replace {from:"sealed_sword",to:"sword_kirion"}
scoreboard players set @s kirionKills 0
function rlk:items/equip_scan
execute at @e[tag=rlk_body,limit=1] run function rlk:items/proc/kirion_fx
