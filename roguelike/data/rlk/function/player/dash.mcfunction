execute if score #charN tmp matches 3 if score @s skDash matches 1.. run return 0
execute if score @s rdCam matches 1 run return 0
execute if score @s pmMoveLock matches 1 run return 0
# 닷지 발동 시도 (@s = 플레이어, at @s; 우클릭 = combat/rclick_do). 충전 없이 재사용 대기 #dashCoolT 틱(질주 2개면 짧아짐)
execute if score @s dashCool matches 1.. run return run function rlk:player/dash_fail
scoreboard players operation @s dashCool = #dashCoolT tmp
function rlk:player/dash_go
