# 결정 축포 발사 (@s = 플레이어, at 몸): 결정 파편을 모두 소모 → 장미탄 5/7/9/11발(꿰뚫음) → 적마다 맞은 발수로 피해
scoreboard players remove @s nvC 1
scoreboard players set @s nvFcd 4
scoreboard players operation #nvU tmp = @s nvS
scoreboard players set @s nvS 0
scoreboard players reset 결정파편 stacks
# 충전이 다 차 있었으면 지금부터 다음 충전 시작(재사용 대기 감소 효과 반영)
execute if score @s nvC matches 1 run scoreboard players set @s nvCT 0
scoreboard players operation @s skillCd = #nvCd tmp
function rlk:char/cd_reduce
scoreboard players operation @s nvCdE = @s skillCd
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
execute if score #nvU tmp matches 0 anchored eyes positioned ^ ^-0.2 ^0.6 run function rlk:char/navia/fan_5
execute if score #nvU tmp matches 1 anchored eyes positioned ^ ^-0.2 ^0.6 run function rlk:char/navia/fan_7
execute if score #nvU tmp matches 2 anchored eyes positioned ^ ^-0.2 ^0.6 run function rlk:char/navia/fan_9
execute if score #nvU tmp matches 3.. anchored eyes positioned ^ ^-0.2 ^0.6 run function rlk:char/navia/fan_11
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
execute as @e[tag=rlk_mob,scores={nvHit=1..}] at @s run function rlk:char/navia/rose_hit
scoreboard players operation @s critChance -= #nvCr tmp
execute if score #hitLanded tmp matches 1 run function rlk:char/particles {n:2,el:5}
function rlk:char/after_hit
# 고유 특성: 일반 공격이 바위 원소로
scoreboard players operation @s nvP = #nvPDur tmp
# 우산총 · 소리
execute unless entity @e[tag=rlk_nvgun,limit=1] run function rlk:char/navia/gun_spawn
scoreboard players set @s nvGun 14
# 우산이 펴진다
function rlk:char/navia/gun_open
execute anchored eyes run particle minecraft:explosion ^ ^-0.2 ^1.4 0 0 0 0 1
execute anchored eyes run particle minecraft:wax_on ^ ^-0.2 ^1.6 0.4 0.4 0.4 0 16
playsound minecraft:entity.firework_rocket.blast master @a ~ ~ ~ 1.0 0.6
playsound minecraft:entity.generic.explode master @a ~ ~ ~ 0.5 1.5
playsound minecraft:block.amethyst_block.break master @a ~ ~ ~ 0.8 0.9
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
function rlk:items/hook/on_cast_skill
function rlk:combat/on_skill
