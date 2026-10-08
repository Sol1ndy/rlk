# 3타의 두 번째 참격 (@s = 플레이어, at 몸): 공격력의 65%. combat/find 의 피해 부분과 같다
scoreboard players set #basic itv 1
scoreboard players set #skDepUsed tmp 0
execute store result score #rng tmp run random value 1..100
scoreboard players set #crit tmp 0
execute if score #rng tmp <= @s critChance run scoreboard players set #crit tmp 1
function rlk:engravings/keen/roll
scoreboard players set #coef tmp 65
scoreboard players operation #dmg tmp = @s atk
scoreboard players operation #dmg tmp *= #coef tmp
scoreboard players operation #dmg tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players operation #elem tmp = @s infuse
execute unless score #elem tmp matches 0..7 run scoreboard players set #elem tmp 0
execute if score @s skM matches 1.. run function rlk:char/skirk/na_mode
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
execute unless score #skMode tmp matches 1 as @e[tag=rlk_mob,distance=..3.5] at @s run function rlk:combat/apply_reset
execute if score #skMode tmp matches 1 as @e[tag=rlk_mob,distance=..5] at @s run function rlk:combat/apply_reset
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
scoreboard players set #fxId tmp 15
execute if score @s skM matches 1.. run scoreboard players set #fxId tmp 25
function rlk:char/fx/play
playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 0.4 1.8
execute if score #hitLanded tmp matches 1 run playsound minecraft:entity.player.attack.strong master @a ~ ~ ~ 0.6 0.9
execute if score #hitLanded tmp matches 1 run function rlk:combat/on_hit
execute if score #mobKilled tmp matches 1.. run function rlk:combat/on_kill
execute if score #skDepUsed tmp matches 1 if score #hitLanded tmp matches 1 run function rlk:char/skirk/dep_use
scoreboard players set #basic itv 0
