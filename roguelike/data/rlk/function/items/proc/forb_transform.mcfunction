# @s = 플레이어, at @s. 금단의 도서 1개 → 데모노미콘 + 카운터 리셋 + 이펙트
function rlk:items/order_replace {from:"forbidden_book",to:"demonomicon"}
scoreboard players set @s forbPages 0
scoreboard players set @s bookPages 0
function rlk:items/equip_scan
execute at @e[tag=rlk_body,limit=1] run function rlk:items/proc/forb_fx
