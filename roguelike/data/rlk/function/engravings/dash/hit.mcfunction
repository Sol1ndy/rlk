# @s = 플레이어, 위치 = 몸. 근처(2.2칸)의 아직 안 맞은 적에게 공격력의 80퍼센트 바람 원소 피해 (스킬 피해로 치지 않음)
function rlk:char/dmg_calc {coef:80}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 6
scoreboard players set #elU tmp 1000
tag @e[tag=rlk_mob,tag=!rlk_dhit,distance=..2.2] add rlk_dnow
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_dnow] at @s run function rlk:combat/apply_reset
execute at @e[tag=rlk_dnow] run particle minecraft:gust ~ ~1 ~ 0.2 0.3 0.2 0 1
tag @e[tag=rlk_dnow] add rlk_dhit
tag @e[tag=rlk_dnow] remove rlk_dnow
playsound minecraft:entity.breeze.wind_burst master @a ~ ~ ~ 0.5 1.6
function rlk:char/after_hit
