# 패링 · 닷지 판정 (@s = 플레이어, at 몸 anchored eyes; player/take_damage 와 mboss/hz/hurt_pm 이 피해를 넣기 전에 부름). 피해 문맥
# (한 번 쓰고 지우는 tmp 점수 · 태그, 피해 입구가 정함: player/def/ctx_*, mboss/hurt):
#   #hcK 공격 종류 1 근접 · 2 투사체 · 3 범위(0 = 모름: 바닐라) / #hcC 공격자 등급 0 일반 · 1 정예 · 2 보스(중간 · 챕터 · 특수 · 나루카미)
#   #hcNP 1 = 패링 불가 / #hcND 1 = 닷지 · 무적으로 못 피함 / 태그 rlk_hc_atk = 공격한 적(균형치를 깎을 몸; 없으면 없음)
# 출력: #dodged tmp 1 = 피해 없음(무적 · 닷지 · 3단계 패링), #parT tmp 0-3 = 패링 단계, #pdg tmp 1 = 퍼펙트 닷지.
# 2단계 · 1단계는 피해를 줄이고(player/take_damage, 원소 반응 뒤 player/def/par_keep) 맞은 것으로 둔다.
# 순서: 무적(dashInvT) > 퍼펙트 닷지 > 3단계 패링 > 넓은 닷지(일반 몹) > 2단계 > 1단계 > 맞음. 누른 틱 = 0 의 틱 수:
#   닷지 d = 지금 - dgAt, 패링 p = 지금 - parAt(아직 막지 않은 F, 또는 이번 틱에 막은 F: 한 번 누름 = 한 틱의 공격들)
scoreboard players operation #jK tmp = #hcK tmp
scoreboard players operation #jC tmp = #hcC tmp
scoreboard players operation #jNP tmp = #hcNP tmp
scoreboard players operation #jND tmp = #hcND tmp
scoreboard players set #hcK tmp 0
scoreboard players set #hcC tmp 0
scoreboard players set #hcNP tmp 0
scoreboard players set #hcND tmp 0
scoreboard players set #parT tmp 0
scoreboard players set #pdg tmp 0
execute store result score #now cb run time query gametime
# 1. 닷지가 아닌 무적(원소폭발 시전 · 로노바 부활 · 추락 뒤): 닷지로 못 피하는 공격은 무시
execute if score #jND tmp matches 0 if score @s dashInvT matches 1.. run return run function rlk:player/def/inv
# 2. 퍼펙트 닷지(모든 적)
scoreboard players operation #jd tmp = #now cb
scoreboard players operation #jd tmp -= @s dgAt
execute if score #jND tmp matches 0 if score #jd tmp matches 0.. if score #jd tmp < #dgPW tmp run return run function rlk:player/def/pd
# 3. 패링: 쓸 수 있는 F 인가
scoreboard players operation #jp tmp = #now cb
scoreboard players operation #jp tmp -= @s parAt
scoreboard players set #jpv tmp 0
execute if score @s parHit < @s parAt run scoreboard players set #jpv tmp 1
execute if score @s parHit = #now cb run scoreboard players set #jpv tmp 1
execute if score #jNP tmp matches 1 run scoreboard players set #jpv tmp 0
execute if score #jp tmp matches ..-1 run scoreboard players set #jpv tmp 0
execute if score #jpv tmp matches 1 if score #jp tmp < #parW3 tmp run return run function rlk:player/def/par3
# 4. 넓은 닷지: 일반 몹(#dgLooseC 1 이면 정예까지)
execute if score #jND tmp matches 0 if score #jC tmp <= #dgLooseC tmp if score #jd tmp matches 0.. if score #jd tmp < #dgLW tmp run return run function rlk:player/def/loose
# 5. 2단계 · 1단계 패링
execute if score #jpv tmp matches 1 if score #jp tmp < #parW2 tmp run return run function rlk:player/def/par2
execute if score #jpv tmp matches 1 if score #jp tmp < #parW1 tmp run return run function rlk:player/def/par1
# 6. 맞음
tag @e[tag=rlk_hc_atk] remove rlk_hc_atk
