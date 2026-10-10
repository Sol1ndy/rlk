# 유금화광 폭발 (@s = 예약 표식, at @s): 반경 3칸에 공격력의 220% 불 원소 피해(원소폭발 피해로 친다)
tag @e[tag=rlk_mob,distance=..3] add rlk_hit
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:220}
execute as @a[tag=player,limit=1] run function rlk:items/hook/burst_dmg
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
scoreboard players set #yoiBoom tmp 1
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #yoiBoom tmp 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
particle minecraft:explosion ~ ~1 ~ 0.6 0.4 0.6 0 2
particle minecraft:firework ~ ~1 ~ 0.3 0.3 0.3 0.25 40
particle minecraft:flame ~ ~1 ~ 0.9 0.6 0.9 0.08 40
execute unless score #k247 snd matches 1 run function rlk:snd/f274
execute unless score #k93 snd matches 1 run function rlk:snd/f275
