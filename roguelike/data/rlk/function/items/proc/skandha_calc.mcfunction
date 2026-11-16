# @s = 플레이어. 공격력의 #skCoef% + 원소 마스터리의 #skEm‰ (강화 단계로 조정)
execute store result storage rlk:tune m_skandha_seed.coef int 1 run scoreboard players get #skCoef tmp
function rlk:char/dmg_calc with storage rlk:tune m_skandha_seed
scoreboard players operation #t1 itv = @s elemMastery
scoreboard players operation #t1 itv *= #skEm tmp
scoreboard players operation #t1 itv /= #1000 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv /= #100 tmp
scoreboard players operation #dmg tmp += #t1 itv
