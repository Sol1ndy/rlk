particle minecraft:dust{color:[0.77f,0.55f,1.0f],scale:1.5f} ~ ~2.2 ~ 0.08 1.6 0.08 0 30
particle minecraft:electric_spark ~ ~0.8 ~ 0.9 0.5 0.9 0.4 25
execute unless score #k160 snd matches 1 run function rlk:snd/f169
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:50}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..3] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
