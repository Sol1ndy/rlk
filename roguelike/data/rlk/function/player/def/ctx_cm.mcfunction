# 피해 문맥 (@s = 공격한 커스텀 몹 두뇌 · 그 투사체 · 나루카미 위험 지대 표식; cm/hit_pl). 태그 rlk_hc_atk = 균형치를 깎을 몸:
# 두뇌는 자신, 투사체는 같은 cmId 의 두뇌(주인), 나루카미의 지대는 나루카미. 등급: 정예 표시(rlk_c2e · rlk_c3e) 1, 나루카미 2.
# 종류: 부른 쪽이 이미 정했으면(#hcK 1..) 그대로, 아니면 두뇌 1 · 그 밖(투사체) 2. 나루카미 지대의 #hcNP · #hcND · #hcK 는
# boss/raiden/hazard/land 가 정한다. 커스텀 몹의 공격은 모두 패링할 수 있다(패링 불가 = 보스의 일부 큰 공격만).
tag @e[tag=rlk_hc_atk] remove rlk_hc_atk
execute if entity @s[tag=rlk_rd_hazard] run return run function rlk:player/def/ctx_rd
scoreboard players set #hcC tmp 0
execute unless score #hcK tmp matches 1.. if entity @s[tag=rlk_cmb] run scoreboard players set #hcK tmp 1
execute unless score #hcK tmp matches 1.. run scoreboard players set #hcK tmp 2
execute if entity @s[tag=rlk_cmb] run tag @s add rlk_hc_atk
execute unless entity @s[tag=rlk_cmb] if score @s cmId matches 1.. run function rlk:player/def/ctx_owner
execute if entity @e[tag=rlk_hc_atk,tag=rlk_c2e,limit=1] run scoreboard players set #hcC tmp 1
execute if entity @e[tag=rlk_hc_atk,tag=rlk_c3e,limit=1] run scoreboard players set #hcC tmp 1
