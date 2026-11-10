# player/def/judge 의 나머지(무적 · 닷지 · 패링 중 하나라도 창 안일 때). 문맥 #hc* 는 부른 쪽(judge)이 끝에 지운다(player/def/end)
# 1. 닷지가 아닌 무적(원소폭발 시전 · 로노바 부활 · 추락 뒤): 닷지로 못 피하는 공격은 무시
execute if score #hcND tmp matches 0 if score @s dashInvT matches 1.. run return run function rlk:player/def/inv
# 2. 퍼펙트 닷지(모든 적)
execute if score #hcND tmp matches 0 if score #jd tmp matches 0.. if score #jd tmp < #dgPW tmp run return run function rlk:player/def/pd
# 3. 패링: 쓸 수 있는 F 인가
scoreboard players set #jpv tmp 0
execute if score @s parHit < @s parAt run scoreboard players set #jpv tmp 1
execute if score @s parHit = #now cb run scoreboard players set #jpv tmp 1
execute if score #hcNP tmp matches 1 run scoreboard players set #jpv tmp 0
execute if score #jp tmp matches ..-1 run scoreboard players set #jpv tmp 0
execute if score #jpv tmp matches 1 if score #jp tmp < #parW3 tmp run return run function rlk:player/def/par3
# 4. 넓은 닷지: 일반 몹(#dgLooseC 1 이면 정예까지)
execute if score #hcND tmp matches 0 if score #hcC tmp <= #dgLooseC tmp if score #jd tmp matches 0.. if score #jd tmp < #dgLW tmp run return run function rlk:player/def/loose
# 5. 2단계 · 1단계 패링
execute if score #jpv tmp matches 1 if score #jp tmp < #parW2 tmp run return run function rlk:player/def/par2
execute if score #jpv tmp matches 1 if score #jp tmp < #parW1 tmp run return run function rlk:player/def/par1
