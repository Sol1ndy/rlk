# 패링 · 닷지 판정 (@s = 플레이어, at 몸 anchored eyes; player/take_damage 와 mboss/hz/hurt_pm 이 피해를 넣기 전에 부름). 피해 문맥
# (한 번 쓰고 지우는 tmp 점수 · 태그, 피해 입구가 정함: player/def/ctx_*, mboss/hurt_ctx, 나루카미 hazard/land):
#   #hcK 공격 종류 1 근접 · 2 투사체 · 3 범위(0 = 모름: 바닐라) / #hcC 공격자 등급 0 일반 · 1 정예 · 2 보스(중간 · 챕터 · 특수 · 나루카미)
#   #hcNP 1 = 패링 불가 / #hcND 1 = 닷지 · 무적으로 못 피함 / 태그 rlk_hc_atk = 공격한 적(균형치를 깎을 몸; 없으면 없음)
# 출력: #dodged tmp 1 = 피해 없음(무적 · 닷지 · 3단계 패링), #parT tmp 0-3 = 패링 단계, #pdg tmp 1 = 퍼펙트 닷지.
# 2단계 · 1단계는 피해를 줄이고(player/take_damage, 원소 반응 뒤 player/def/par_keep) 맞은 것으로 둔다.
# 순서(player/def/judge2): 무적(dashInvT) > 퍼펙트 닷지 > 3단계 패링 > 넓은 닷지(일반 몹) > 2단계 > 1단계 > 맞음. 누른 틱 = 0 의 틱 수:
#   닷지 d = 지금 - dgAt, 패링 p = 지금 - parAt(아직 막지 않은 F, 또는 이번 틱에 막은 F: 한 번 누름 = 한 틱의 공격들).
# 빠른 길: 무적도 없고 닷지 · F 가 창 밖이면(d >= #dgLW, p >= #parW1) 바로 맞음(문맥만 지움)
execute store result score #now cb run time query gametime
# 시각 도장이 없는 플레이어(전투 개편 전 저장 · 시험 세계): 먼 과거로
execute unless score @s parHit matches -2147483648.. run function rlk:player/def/reset
scoreboard players set #parT tmp 0
scoreboard players set #pdg tmp 0
scoreboard players operation #jd tmp = #now cb
scoreboard players operation #jd tmp -= @s dgAt
scoreboard players operation #jp tmp = #now cb
scoreboard players operation #jp tmp -= @s parAt
execute unless score @s dashInvT matches 1.. if score #jd tmp >= #dgLW tmp if score #jp tmp >= #parW1 tmp run return run function rlk:player/def/end
function rlk:player/def/judge2
function rlk:player/def/end
