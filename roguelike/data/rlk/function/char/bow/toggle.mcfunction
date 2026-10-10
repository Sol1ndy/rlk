# F 키 (@s = 플레이어, at 몸): 조준 시작. 조준 중이면 쏘지 않고 취소
execute if score @s bowT matches 1.. unless score #k237 snd matches 1 run function rlk:snd/f264
execute if score @s bowT matches 1.. run return run function rlk:char/bow/cancel
execute if score @s bowCd matches 1.. run return 0
function rlk:char/bow/start
