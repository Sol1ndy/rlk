# @s = 플레이어. 공격력의 80퍼센트 + 원소 마스터리의 10퍼센트
function rlk:char/dmg_calc {coef:80}
scoreboard players operation #t1 itv = @s elemMastery
scoreboard players operation #t1 itv /= #st10 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv /= #100 tmp
scoreboard players operation #dmg tmp += #t1 itv
