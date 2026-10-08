# 얼음 안개검 (@s = 플레이어, at @s): 전방 부채꼴에 공격력의 #lumSkill% 얼음 원소 피해 + 혹한의 별 생성
function rlk:char/lumine/skill_fx
function rlk:char/dmg_calc {coef:200}
scoreboard players set #elem tmp 4
scoreboard players set #elU tmp 1000
# 부채꼴 판정: 시선 방향(수평)으로 점점 커지는 구 여러 개
tag @e[tag=rlk_mob,distance=..1.6] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^2 run tag @e[tag=rlk_mob,distance=..2.3] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^4 run tag @e[tag=rlk_mob,distance=..3.2] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^6 run tag @e[tag=rlk_mob,distance=..3.7] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
# 적중: 원소 입자 3개
execute if score #hitLanded tmp matches 1 rotated ~ 0 positioned ^ ^1.2 ^3 run function rlk:char/particles {n:3,el:4}
function rlk:char/after_hit
function rlk:char/lumine/star_spawn
# 고유 특성 '예리한 얼음': 8초 동안 기본 공격 강화
scoreboard players set @s lumP 160
