# 두 번 치는 타의 두 번째 참격 (@s = 플레이어, at 몸): 계수 = naQc. combat/find 의 피해 부분과 같다
scoreboard players set #basic itv 1
execute store result score #rng tmp run random value 1..100
scoreboard players set #crit tmp 0
execute if score #rng tmp <= @s critChance run scoreboard players set #crit tmp 1
function rlk:engravings/keen/roll
scoreboard players operation #coef tmp = @s naQc
scoreboard players operation #dmg tmp = @s atk
scoreboard players operation #dmg tmp *= #coef tmp
scoreboard players operation #dmg tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players operation #elem tmp = @s infuse
execute unless score #elem tmp matches 0..8 run scoreboard players set #elem tmp 0
execute if score #charN tmp matches 5 if score @s arM matches 1 run function rlk:char/arlecchino/na_mask
execute if score #charN tmp matches 6 if score @s nvP matches 1.. run function rlk:char/navia/na_geo
execute if score #charN tmp matches 8 unless score @s infuse matches 1..8 run scoreboard players set #elem tmp 7
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
scoreboard players set #tfm tmp 0
scoreboard players set #stunHit tmp 1
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players set #skillDmg tmp 0
scoreboard players operation #dmgBase tmp = #dmg tmp
function rlk:char/melee/range
function rlk:combat/melee_begin
execute if score #naR tmp matches 0 as @e[tag=rlk_mob,distance=..3.5] at @s run function rlk:combat/melee_apply
execute if score #naR tmp matches 1 as @e[tag=rlk_mob,distance=..5] at @s run function rlk:combat/melee_apply
execute if score #naR tmp matches 2 as @e[tag=rlk_mob,distance=..4.5] at @s run function rlk:combat/melee_apply
kill @e[tag=rlk_melee_origin]
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
# 모션: 두 번째 타격
execute if score #charN tmp matches 4 run scoreboard players set #fxId tmp 35
execute if score #charN tmp matches 5 run scoreboard players set #fxId tmp 46
execute if score #charN tmp matches 5 if score @s arM matches 1 run scoreboard players set #fxId tmp 56
execute if score #charN tmp matches 6 run scoreboard players set #fxId tmp 87
execute if score #charN tmp matches 6 if score @s nvP matches 1.. run scoreboard players set #fxId tmp 97
execute if score #charN tmp matches 8 run scoreboard players set #fxId tmp 107
function rlk:char/fx/play
execute unless score #charN tmp matches 5 unless score #charN tmp matches 6 run execute unless score #k310 snd matches 1 run function rlk:snd/f357
execute unless score #charN tmp matches 5 unless score #charN tmp matches 6 run execute if score #hitLanded tmp matches 1 unless score #k311 snd matches 1 run function rlk:snd/f358
execute if score #hitLanded tmp matches 1 run function rlk:combat/on_hit
execute if score #mobKilled tmp matches 1.. run function rlk:combat/on_kill
execute if score #charN tmp matches 5 run function rlk:char/arlecchino/na_post
scoreboard players set #basic itv 0
# 남은 추가 타격
scoreboard players remove @s naQn 1
execute if score @s naQn matches 1.. run scoreboard players set @s naQ 3
