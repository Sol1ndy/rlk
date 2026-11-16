# 반경 3.5칸에 공격력의 #wispCoef% 얼음 원소 피해
execute store result storage rlk:tune m_star_wisp.coef int 1 run scoreboard players get #wispCoef tmp
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc with storage rlk:tune m_star_wisp
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 4
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..3.5] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
