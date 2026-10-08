# 스탯 계수 피해 계산 (@s = 플레이어, macro: obj = 스탯 점수 이름(maxHealth·def 등), pm = 천분율). 치명타 판정 포함 — char/dmg_calc 의 스탯판
function rlk:char/dmg_calc {coef:0}
$scoreboard players operation #dmg tmp = @s $(obj)
$scoreboard players set #t9 itv $(pm)
scoreboard players operation #dmg tmp *= #t9 itv
scoreboard players operation #dmg tmp /= #1000 tmp
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp /= #100 tmp
