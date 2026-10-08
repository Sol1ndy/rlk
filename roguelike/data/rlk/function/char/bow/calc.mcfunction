# 화살 한 발의 피해 계산 (@s = 플레이어, 입력 #coef tmp = 공격력의 %). 치명타는 발마다 판정. 결과 #dmg #crit
execute store result score #rng tmp run random value 1..100
scoreboard players set #crit tmp 0
execute if score #rng tmp <= @s critChance run scoreboard players set #crit tmp 1
function rlk:engravings/keen/roll
scoreboard players operation #dmg tmp = @s atk
scoreboard players operation #dmg tmp *= #coef tmp
scoreboard players operation #dmg tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp /= #100 tmp
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
