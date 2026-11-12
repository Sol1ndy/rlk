execute unless score #k197 snd matches 1 run function rlk:snd/f213
# 피해 = 최대 체력의 #salonPm‰ (강화 단계로 조정)
data modify storage rlk:tune m_salon_invite.obj set value "maxHealth"
execute store result storage rlk:tune m_salon_invite.pm int 1 run scoreboard players get #salonPm tmp
execute as @a[tag=player,limit=1] run function rlk:items/calc_stat with storage rlk:tune m_salon_invite
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
scoreboard players operation #t1 itv = #salonI itv
execute as @e[tag=rlk_salon] if score @s smI = #t1 itv run tag @s add rlk_salon_cur
execute at @e[tag=rlk_salon_cur,limit=1] facing entity @e[tag=rlk_abt,limit=1] eyes run function rlk:items/fx/shot
execute at @e[tag=rlk_salon_cur,limit=1] run particle minecraft:splash ~ ~ ~ 0.15 0.15 0.15 0 12
tag @e[tag=rlk_salon_cur] remove rlk_salon_cur
scoreboard players add #salonI itv 1
execute if score #salonI itv matches 3.. run scoreboard players set #salonI itv 0
tag @e[tag=rlk_abt] remove rlk_abt
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..12,sort=nearest,limit=1] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
