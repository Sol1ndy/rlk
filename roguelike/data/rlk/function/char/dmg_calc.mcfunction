# 스킬 피해 계산 (@s = 플레이어, macro: coef = 공격력의 %). 치명타 판정 포함. 결과 #dmg #crit + 공격 플래그 초기화(스킬 피해 표시)
execute store result score #rng tmp run random value 1..100
scoreboard players set #crit tmp 0
execute if score #rng tmp <= @s critChance run scoreboard players set #crit tmp 1
# 각인 예리 6개: 확정 치명타
function rlk:engravings/keen/roll
$scoreboard players set #coef tmp $(coef)
scoreboard players operation #dmg tmp = @s atk
scoreboard players operation #dmg tmp *= #coef tmp
scoreboard players operation #dmg tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp /= #100 tmp
function rlk:combat/clear_atkflags
scoreboard players set #skillDmg tmp 1
scoreboard players set #stunHit tmp 1
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
