# @s = 플레이어. 공격력의 400퍼센트 + 최대 체력의 20퍼센트 (치명타 판정 한 번)
function rlk:char/dmg_calc {coef:400}
scoreboard players operation #t1 itv = @s maxHealth
scoreboard players operation #t1 itv *= #st20 tmp
scoreboard players operation #t1 itv /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv /= #100 tmp
scoreboard players operation #dmg tmp += #t1 itv
