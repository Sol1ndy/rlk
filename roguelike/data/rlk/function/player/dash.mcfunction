execute if score #charN tmp matches 3 if score @s skDash matches 1.. run return 0
execute if score @s rdCam matches 1 run return 0
execute if score @s pmMoveLock matches 1 run return 0
# 닷지 발동 시도 (@s = 플레이어, at @s; 우클릭 = combat/rclick_do). 충전 없이 재사용 대기 #dashCoolT 틱(아무것도 피하지 못한 닷지 18틱;
# 공격을 피하면 player/def/dg_refund 가 #dashCoolHitT 12틱이 되게 돌려줌; 질주 2개면 14 / 10)
# 이 시도의 시각(#dgTry cb)과 바로 앞 시도부터의 틱 수(#dgTryD cb): 누르고 있어 4틱마다 반복되는 우클릭의 실패 소리를 가린다(player/dash_fail)
execute store result score #t cb run time query gametime
scoreboard players operation #dgTryD cb = #t cb
scoreboard players operation #dgTryD cb -= #dgTry cb
scoreboard players operation #dgTry cb = #t cb
execute if score @s dashCool matches 1.. run return run function rlk:player/dash_fail
scoreboard players operation @s dashCool = #dashCoolT tmp
function rlk:player/dash_go
