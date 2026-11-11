# @s = 플레이어, at 몸 (player/dash: 재사용 대기 중의 누름; #t cb = 지금 gametime). 더블 닷지의 두 번째 누름인가: 이번 세트의 첫 스텝
# (#dgN cb 1)을 누른 지 1 ~ #dgChW 틱(전투 시계: 박자가 세계를 멈춘 틱은 세지 않음)이면 두 번째 동작 — 공중 옆돌기 — 을 시작한다.
# 새 닷지 도장(= 새 퍼펙트 창 · 넓은 창 · 시작 자리 상자)을 찍고 재사용 대기를 #dashCoolT 만큼 더한다: 닷지 창을 여는 빈도는 예전과 같다
# (창 둘에 재사용 대기 둘; 피한 닷지마다 player/def/dg_refund 가 한 번씩 돌려줌). 한 세트에 한 번뿐. 아니면 재사용 대기 중의 실패 소리
execute unless score #dgN cb matches 1 run return run function rlk:player/dash_fail
# F5 에서 우클릭을 누르고 있어 4틱마다 반복되는 것(combat/rc_hold 의 #rcRep)은 두 번째 누름이 아니다: 손을 뗐다 다시 눌러야 한다
execute if score #rcRep tmp matches 1 run return run function rlk:player/dash_fail
scoreboard players operation #t cb -= #btAdj cb
scoreboard players operation #t cb -= @s dgAt
execute if score #t cb matches ..0 run return run function rlk:player/dash_fail
execute if score #t cb > #dgChW tmp run return run function rlk:player/dash_fail
scoreboard players operation @s dashCool += #dashCoolT tmp
# 첫 동작이 공격을 피해 백스텝이 되었으면(#dgMv 4) 옆돌기는 그 방향으로 이어진다(player/dash_go)
scoreboard players operation #dgPrev cb = #dgMv cb
scoreboard players set #dgMv cb 2
scoreboard players set #dgN cb 2
function rlk:player/dash_go
