particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.3 14
playsound minecraft:entity.wolf.growl master @a ~ ~ ~ 0.5 1.5
particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 2
particle minecraft:dust{color:[0.77f,0.55f,1.00f],scale:1.5f} ~ ~1 ~ 0.3 0.3 0.3 0 12
particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.4 10
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:35}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_ht] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute as @a[tag=player,limit=1] run function rlk:items/proc/hound_heal
