# 기본공격 처리 (@s = 공격한 플레이어, at @s)
# 네페르: 그림자 춤 중 풀 이슬이 있으면 환영극
execute if score #charN tmp matches 8 if score @s nfSD matches 1.. if score @s nfDew matches 1.. run return run function rlk:char/nefer/phantasm
# 이번 타(콤보 단계)의 계수: 캐릭터의 1타 #na1 / 2타 #na2 (%)
scoreboard players operation #coef tmp = #na1 tmp
execute if score @s comboStep matches 1 run scoreboard players operation #coef tmp = #na2 tmp
# 다음 타까지 간격의 %(캐릭터의 na_coef 가 타마다 바꾼다. 평균 100)
scoreboard players set #naD tmp 100
# 스커크: 5타 콤보의 계수
execute if score #charN tmp matches 3 run function rlk:char/skirk/na_coef
# 클로린드 · 아를레키노: 공통 콤보(char/melee)의 계수
scoreboard players set #naX2 tmp 0
execute if score #charN tmp matches 4 run function rlk:char/clorinde/na_coef
execute if score #charN tmp matches 5 run function rlk:char/arlecchino/na_coef
execute if score #charN tmp matches 6 run function rlk:char/navia/na_coef
execute if score #charN tmp matches 8 run function rlk:char/nefer/na_coef
# 각인 연격: 이번이 2타인지 기억
scoreboard players set #fl2 eng 0
execute if score @s comboStep matches 1 run scoreboard players set #fl2 eng 1
scoreboard players set #basic itv 1
function rlk:combat/do_swing
# 치명타 판정
execute store result score #rng tmp run random value 1..100
scoreboard players set #crit tmp 0
execute if score #rng tmp <= @s critChance run scoreboard players set #crit tmp 1
# 각인 예리 6개: 확정 치명타
function rlk:engravings/keen/roll
# 데미지 = 공격력 × 계수% (치명타 시 × 치명타 피해%)
scoreboard players operation #dmg tmp = @s atk
scoreboard players operation #dmg tmp *= #coef tmp
scoreboard players operation #dmg tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp /= #100 tmp
# (공격자 기준 데미지 보정은 여기에 추가)
# 원소: 원소 부여(infuse) 상태면 그 원소로, 아니면 물리. 기본공격은 부착 쿨(2.5초 또는 3타) 적용
scoreboard players operation #elem tmp = @s infuse
execute unless score #elem tmp matches 0..8 run scoreboard players set #elem tmp 0
# 캐릭터 고유 특성(기본 공격 보정)
execute if score #charN tmp matches 1 if score @s lumP matches 1.. run function rlk:char/lumine/na_passive
execute if score #charN tmp matches 3 if score @s skM matches 1.. run function rlk:char/skirk/na_mode
execute if score #charN tmp matches 5 if score @s arM matches 1 run function rlk:char/arlecchino/na_mask
execute if score #charN tmp matches 6 if score @s nvP matches 1.. run function rlk:char/navia/na_geo
execute if score #charN tmp matches 8 unless score @s infuse matches 1..8 run scoreboard players set #elem tmp 7
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
scoreboard players set #tfm tmp 0
scoreboard players set #lunar tmp 0
scoreboard players set #stunHit tmp 1
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players set #skillDmg tmp 0
# 전방 범위 공격: 기존 사거리 안에서 몸이 바라보는 앞쪽 180도만 타격 (몹별 증폭 복리 방지: 대상마다 기본 데미지에서 시작)
scoreboard players operation #dmgBase tmp = #dmg tmp
# 스커크의 일곱빛 섬광 중에는 범위가 넓다(3.5칸 → 5칸)
# 범위(#naR): 0 = 3.5칸, 1 = 5칸(스커크의 일곱빛 섬광), 2 = 4.5칸(장병기)
function rlk:char/melee/range
function rlk:combat/melee_begin
execute if score #naR tmp matches 0 as @e[tag=rlk_mob,distance=..3.5] at @s run function rlk:combat/melee_apply
execute if score #naR tmp matches 1 as @e[tag=rlk_mob,distance=..5] at @s run function rlk:combat/melee_apply
execute if score #naR tmp matches 2 as @e[tag=rlk_mob,distance=..4.5] at @s run function rlk:combat/melee_apply
kill @e[tag=rlk_melee_origin]
# 효과음: 스윙(항상) + 타격 시 둔탁 추가 + 치명타 핑 추가
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 unless score #k23 snd matches 1 run function rlk:snd/f23
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 unless score #k24 snd matches 1 run function rlk:snd/f24
# 아를/스커크는 combat/apply의 실제 피해 경로에서 타격음을 냄(헛손질/완전 방어 제외).
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 if score #hitLanded tmp matches 1 unless score #k25 snd matches 1 run function rlk:snd/f25
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 if score #hitLanded tmp matches 1 unless score #k26 snd matches 1 run function rlk:snd/f26
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 if score #hitLanded tmp matches 1 if score #crit tmp matches 1 unless score #k27 snd matches 1 run function rlk:snd/f27
execute if score #hitLanded tmp matches 1 run function rlk:combat/on_hit
execute if score #mobKilled tmp matches 1.. run function rlk:combat/on_kill
execute if score #charN tmp matches 3 run function rlk:char/skirk/na_post
execute if score #charN tmp matches 4..6 run function rlk:char/melee/post
execute if score #charN tmp matches 8 run function rlk:char/melee/post
# 기본공격 시 발동(적중 여부 무관)
function rlk:items/hook/on_basic_attack
# 각인 연격 4개: 2타가 한 번 더 적중
execute if score #fl2 eng matches 1 if score flurry engN matches 4.. run function rlk:engravings/flurry/extra
scoreboard players set #basic itv 0
