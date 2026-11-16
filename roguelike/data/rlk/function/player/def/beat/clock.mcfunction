# 박자(beat)의 시계 (rlk:tick 맨 앞, 박자가 도는 동안만: #btK cb 1 = 퍼펙트 패링, 2 = 퍼펙트 닷지). 실제 틱마다 나이 #btA 를 하나 올리고
# 이번 틱의 세 가지를 정한다:
#   #btHold cb 1 = 세계를 멈춘 틱(적의 패턴 시계 · 리그 · 위험 지대 · 투사체 · 몹의 타이머가 이 틱에 돌지 않음: mboss/main · cm/world ·
#                  cm/pj/world · 나루카미 · mob/tick 의 타이머 · mboss/near_all · 닷지 재사용 대기)
#   #btInv cb 1  = 플레이어가 맞지 않는 틱(player/def/judge2 · player/hurt_elem · mboss/pl_dot2)
#   #btAdj cb    = 전투 시계의 보정(지금까지 멈춘 틱 수 #btLag − 이번 틱이 멈춘 틱이면 1): #now cb = gametime − #btAdj = 다음에 도는 세계 틱의
#                  번호. 멈춘 동안의 F · 닷지는 풀리는 틱에 누른 것으로 친다(창 · 잠금 · 재사용 대기는 멈추지 않은 세계의 틱 수 그대로)
# 박자가 끝나야 하는 상태(플레이어 없음 · 사망 · 부활 대기 · 선택 공간 · 지도 · 연출 카메라)면 바로 끝낸다: 아무것도 멈춘 채 남지 않는다
scoreboard players add #btA cb 1
execute unless entity @a[tag=player,limit=1] run return run function rlk:player/def/beat/end
execute if entity @a[tag=player,scores={dead=1}] run return run function rlk:player/def/beat/end
execute if entity @a[tag=player,scores={rnDie=1..}] run return run function rlk:player/def/beat/end
execute if entity @a[tag=player,scores={pkMode=1..}] run return run function rlk:player/def/beat/end
execute if entity @a[tag=player,scores={vMap=1}] run return run function rlk:player/def/beat/end
execute if entity @a[tag=player,scores={rdCam=1}] run return run function rlk:player/def/beat/end
execute if score #mbCam mb matches 1 run return run function rlk:player/def/beat/end
execute if score #mbCine mb matches 1 run return run function rlk:player/def/beat/end
execute if entity @a[tag=rlk_mb_camh,limit=1] run return run function rlk:player/def/beat/end
execute if score #btK cb matches 1 run return run function rlk:player/def/beat/p/clock
function rlk:player/def/beat/d/clock
