execute if score #charN tmp matches 3 if score @s skDash matches 1.. run return 0
execute if score @s rdCam matches 1 run return 0
execute if score @s pmMoveLock matches 1 run return 0
# 닷지 발동 시도 (@s = 플레이어, at @s; 우클릭 = combat/rclick_do). round W(사용자: 「기존의 '대쉬'는 없어지는거야. 스텔라블레이드의 닷지로
# 완전히 전환」): 긴 대쉬(3칸 / 3틱)는 없다. 닷지 = 원작의 닷지 한 벌 —
#   일반 닷지   짧고 빠른 회피 스텝(이동 방향, 없으면 시선 방향으로 1칸 / 3틱; player/dash_go, #dgMv cb 1)
#   더블 닷지   그 스텝을 누른 지 1 ~ #dgChW 틱 안에 한 번 더 누르면 이어지는 공중 옆돌기(1.8칸 / 6틱; player/dodge/again, #dgMv cb 2)
#   퍼펙트 닷지 어느 쪽이든 누른 지 #dgPW 틱 안에 맞을 공격을 피함(player/def/judge → 박자 player/def/beat/start_d)
# 충전 없이 재사용 대기 #dashCoolT 틱(아무것도 피하지 못한 닷지 18틱; 공격을 피하면 player/def/dg_refund 가 #dashCoolHitT 12틱이 되게
# 돌려줌; 질주 2개면 14 / 10). 더블 닷지의 두 번째 누름은 재사용 대기 중에 받고 재사용 대기를 한 번 더 더한다(둘 다 헛되면 36틱).
# 이 시도의 시각(#dgTry cb)과 바로 앞 시도부터의 틱 수(#dgTryD cb): 누르고 있어 4틱마다 반복되는 우클릭의 실패 소리를 가린다(player/dash_fail)
execute store result score #t cb run time query gametime
scoreboard players operation #dgTryD cb = #t cb
scoreboard players operation #dgTryD cb -= #dgTry cb
scoreboard players operation #dgTry cb = #t cb
execute if score @s dashCool matches 1.. run return run function rlk:player/dodge/again
scoreboard players operation @s dashCool = #dashCoolT tmp
scoreboard players set #dgMv cb 1
function rlk:player/dash_go
