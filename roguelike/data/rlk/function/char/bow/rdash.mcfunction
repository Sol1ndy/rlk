# 활을 든 채 우클릭 (@s = 플레이어, at 몸): 대쉬. 조준 중이면 취소하고 대쉬(대쉬를 쓸 수 없을 때는 조준을 유지)
execute if score @s bowT matches 1.. if score @s dashCharge matches 1.. unless score @s dashCool matches 1.. run function rlk:char/bow/cancel
function rlk:player/dash
