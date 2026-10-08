# @s = 플레이어, 위치 = 몸. 반경 4칸의 적을 띄워 올리고(보스 제외) 공격력의 150퍼센트 바람 원소 피해
particle minecraft:gust_emitter_small ~ ~0.5 ~ 1.5 0.2 1.5 0 4
playsound minecraft:entity.wind_charge.wind_burst master @a ~ ~ ~ 0.9 1.0
execute as @e[tag=rlk_mob,tag=!boss,distance=..4] run data merge entity @s {Motion:[0.0d,0.75d,0.0d]}
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:150}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 6
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..4] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
