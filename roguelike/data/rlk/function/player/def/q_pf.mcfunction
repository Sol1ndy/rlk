# @s = 플레이어, #qn cb = 볼 틱. 그 틱이 닷지의 퍼펙트 창(dgAt + 0..#dgPW-1) 또는 F 의 3단계 창(parAt + 0..#parW3-1) 안이면 1.
# 닷지의 창이면 그 닷지는 공격을 피한 것으로 친다(player/def/q_dg: 재사용 대기를 한 번 돌려줌 — 판정(judge)을 거치지 않고 이 물음만
# 쓰는 공격도 "피한 닷지 12틱"이 되게: 홍련의 연참은 닷지만으로도 12틱 간격을 넘는다)
scoreboard players operation #q cb = #qn cb
scoreboard players operation #q cb -= @s dgAt
execute if score #q cb matches 0.. if score #q cb < #dgPW tmp run return run function rlk:player/def/q_dg
scoreboard players operation #q cb = #qn cb
scoreboard players operation #q cb -= @s parAt
execute if score #q cb matches 0.. if score #q cb < #parW3 tmp run return 1
return fail
