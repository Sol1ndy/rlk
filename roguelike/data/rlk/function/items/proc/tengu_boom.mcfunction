# 반경 3.5칸에 공격력의 #tenguCoef 퍼센트 번개 원소 피해 (피해 계수는 강화 단계로 조정)
execute store result storage rlk:tune m_tengu_feather.coef int 1 run scoreboard players get #tenguCoef tmp
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc with storage rlk:tune m_tengu_feather
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..3.5] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
