playsound minecraft:entity.player.splash master @a ~ ~ ~ 0.25 1.8
execute as @a[tag=player,limit=1] run function rlk:items/calc_stat {obj:"maxHealth",pm:60}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 2
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
# 체력이 절반 넘게 남아 있으면 체력을 잃고 피해 증가
execute as @a[tag=player,limit=1] run function rlk:items/proc/salon_pay
tag @e[tag=rlk_hit,limit=1] add rlk_abt
scoreboard players set #aqE eng 2
scoreboard players set #bi eng 0
execute positioned ~ ~2.4 ~ facing entity @e[tag=rlk_abt,limit=1] eyes run function rlk:items/fx/shot
tag @e[tag=rlk_abt] remove rlk_abt
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..12,sort=nearest,limit=1] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
