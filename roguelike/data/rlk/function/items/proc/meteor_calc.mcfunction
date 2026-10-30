# @s = 플레이어. 공격력의 #meteorCoef% + 최대 체력의 #meteorHp% (강화 단계로 조정, 치명타 판정 한 번)
execute store result storage rlk:tune m_jade_shard.coef int 1 run scoreboard players get #meteorCoef tmp
function rlk:char/dmg_calc with storage rlk:tune m_jade_shard
scoreboard players operation #t1 itv = @s maxHealth
scoreboard players operation #t1 itv *= #meteorHp tmp
scoreboard players operation #t1 itv /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv /= #100 tmp
scoreboard players operation #dmg tmp += #t1 itv
