# @s = 플레이어, at 눈. 그룹 감지 + 버튼 호버 감지
scoreboard players set #ray tmp 0
function rlk:ditem/aim_step
execute if score @s aimingDrop matches 1 run function rlk:ditem/aim_btn
