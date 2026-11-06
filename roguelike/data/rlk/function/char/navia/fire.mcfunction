# 결정 축포 발사 (@s = 플레이어, at 몸, 발사 방향 = char/navia/fire_dir 가 정함): 결정 파편을 모두 소모 → 장미탄 5/7/9/11발(꿰뚫음) → 적마다 맞은 발수로 피해
# 모션 이벤트가 발사 틱에 char/navia/fire_dir 로 부른다(events/navia/skill 7틱 · skill_fire 3틱). 충전은 누른 순간 char/navia/spend 가 소모
scoreboard players set @s nvShot 0
scoreboard players operation #nvU tmp = @s nvS
scoreboard players set @s nvS 0
scoreboard players reset 결정파편 stacks
# 고유 특성: 소모한 파편 1개당 원소 에너지 1pt · 치명타 확률 +12%(최대 36%)
scoreboard players operation #t1 tmp = #nvU tmp
scoreboard players operation #t1 tmp *= #100 tmp
scoreboard players operation @s energy += #t1 tmp
scoreboard players operation #nvCr tmp = #nvU tmp
execute if score #nvCr tmp matches 4.. run scoreboard players set #nvCr tmp 3
scoreboard players operation #nvCr tmp *= #c12 tmp
scoreboard players operation @s critChance += #nvCr tmp
# 장미탄
scoreboard players set @e[tag=rlk_mob] nvHit 0
execute if score #nvU tmp matches 0 positioned ~ ~1.62 ~ positioned ^ ^-0.2 ^0.6 run function rlk:char/navia/fan_5
execute if score #nvU tmp matches 1 positioned ~ ~1.62 ~ positioned ^ ^-0.2 ^0.6 run function rlk:char/navia/fan_7
execute if score #nvU tmp matches 2 positioned ~ ~1.62 ~ positioned ^ ^-0.2 ^0.6 run function rlk:char/navia/fan_9
execute if score #nvU tmp matches 3.. positioned ~ ~1.62 ~ positioned ^ ^-0.2 ^0.6 run function rlk:char/navia/fan_11
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
# 장미탄 피격에는 회색 바닐라 타격 입자(crit · sweep_attack)를 그리지 않는다(combat/apply)
scoreboard players set #noHitFx tmp 1
execute as @e[tag=rlk_mob,scores={nvHit=1..}] at @s run function rlk:char/navia/rose_hit
scoreboard players set #noHitFx tmp 0
scoreboard players operation @s critChance -= #nvCr tmp
execute if score #hitLanded tmp matches 1 run function rlk:char/particles {n:2,el:5}
function rlk:char/after_hit
# 고유 특성: 일반 공격이 바위 원소로
scoreboard players operation @s nvP = #nvPDur tmp
# 우산총(1인칭에서만, 숄더뷰는 모션의 우산 모델) · 총구 효과(시선 높낮이를 따름) · 발사 소리(게임 쪽이 소유, 모션 소리에는 넣지 않음)
execute unless score @s pmVisible matches 1 unless entity @e[tag=rlk_nvgun,limit=1] run function rlk:char/navia/gun_spawn
execute unless score @s pmVisible matches 1 run scoreboard players set @s nvGun 14
# 우산이 펴진다
execute unless score @s pmVisible matches 1 run function rlk:char/navia/gun_open
# 총구 효과(금빛 별 섬광 · 빛무리 · 원뿔 끝 고리 카드 + 폭발 · 반짝임 입자): 숄더뷰는 몸 디스플레이의 우산 끝, 1인칭은 블록 우산총 끝
execute if score @s pmVisible matches 1 positioned ~ ~1.12 ~ positioned ^-0.3 ^ ^ run function rlk:char/navia/muzzle_rig
execute unless score @s pmVisible matches 1 positioned ~ ~1.62 ~ positioned ^-0.42 ^-0.46 ^ run function rlk:char/navia/muzzle_fp
# 발사음: 폭죽 폭발(갈라지는 소리) · 폭발(몸통) · 자수정 깨짐(결정 파편) + 낮은 바람 폭발(압력 쿵)
execute unless score #k226 snd matches 1 run function rlk:snd/f250
execute unless score #k37 snd matches 1 run function rlk:snd/f251
execute unless score #k142 snd matches 1 run function rlk:snd/f252
execute unless score #k351 snd matches 1 run function rlk:snd/f421
function rlk:items/hook/on_cast_skill
function rlk:combat/on_skill
