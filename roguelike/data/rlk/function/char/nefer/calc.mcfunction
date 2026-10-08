# 네페르 피해 계산 (@s = 플레이어, macro: a = 공격력의 %, e = 원소 마스터리의 %). dmg_calc 처럼 치명타 · 공격 플래그 초기화
$function rlk:char/dmg_calc {coef:$(a)}
execute store result score #t1 tmp run scoreboard players get @s elemMastery
execute if score #t1 tmp matches ..-1 run scoreboard players set #t1 tmp 0
$scoreboard players set #t2 tmp $(e)
scoreboard players operation #t1 tmp *= #t2 tmp
scoreboard players operation #t1 tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #t1 tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #t1 tmp /= #100 tmp
scoreboard players operation #dmg tmp += #t1 tmp
