execute if score #charN tmp matches 3 if score @s skDash matches 1.. run return 0
execute if score @s rdCam matches 1 run return 0
execute if score @s pmMoveLock matches 1 run return 0
# 대쉬 발동 시도 (@s = 플레이어, at @s)
# 충전식: 최대 #dashMax 개 보유, 1개 충전에 #dashRegenT 틱, 대쉬 직후 자체 쿨타임 #dashCoolT 틱 (값은 load 에서 설정)
execute if score @s dashCool matches 1.. run return 0
execute unless score @s dashCharge matches 1.. run return run function rlk:player/dash_fail
scoreboard players remove @s dashCharge 1
scoreboard players operation @s dashCool = #dashCoolT tmp
function rlk:player/dash_go
