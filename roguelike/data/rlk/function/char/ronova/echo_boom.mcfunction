# 잔향 폭발 (@s = 잔향 투사체, at @s): 반경 2.5칸에 그 원소 피해(원소전투 스킬 피해, 부착 1U). 여기서 일어난 반응은 잔향을 남기지 않는다
scoreboard players set #jend tmp 1
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = @s jdmg
scoreboard players operation #crit tmp = @s jcrit
scoreboard players operation #elem tmp = @s aEl
scoreboard players set #elU tmp 1000
scoreboard players set #skillDmg tmp 1
scoreboard players set #stunHit tmp 1
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players set #rnNoEcho tmp 1
execute at @s run tag @e[tag=rlk_mob,distance=..2.5] add rlk_hit
scoreboard players set @e[tag=rlk_hit] rnNoE 200
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #rnNoEcho tmp 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute at @s run particle minecraft:explosion ~ ~ ~ 0 0 0 0 1
execute at @s if score @s aEl matches 1 run particle minecraft:dust{color:[1.00,0.50,0.20],scale:1.4} ~ ~ ~ 1.0 0.6 1.0 0 30
execute at @s if score @s aEl matches 2 run particle minecraft:dust{color:[0.30,0.60,1.00],scale:1.4} ~ ~ ~ 1.0 0.6 1.0 0 30
execute at @s if score @s aEl matches 3 run particle minecraft:dust{color:[0.75,0.45,1.00],scale:1.4} ~ ~ ~ 1.0 0.6 1.0 0 30
execute at @s if score @s aEl matches 4 run particle minecraft:dust{color:[0.70,0.95,1.00],scale:1.4} ~ ~ ~ 1.0 0.6 1.0 0 30
execute at @s if score @s aEl matches 5 run particle minecraft:dust{color:[1.00,0.80,0.30],scale:1.4} ~ ~ ~ 1.0 0.6 1.0 0 30
execute at @s if score @s aEl matches 6 run particle minecraft:dust{color:[0.45,0.90,0.75],scale:1.4} ~ ~ ~ 1.0 0.6 1.0 0 30
execute at @s if score @s aEl matches 7 run particle minecraft:dust{color:[0.60,0.85,0.30],scale:1.4} ~ ~ ~ 1.0 0.6 1.0 0 30
execute at @s if score @s aEl matches 8 run particle minecraft:dust{color:[0.88,0.15,0.30],scale:1.4} ~ ~ ~ 1.0 0.6 1.0 0 30
execute at @s run particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.0} ~ ~ ~ 0.6 0.4 0.6 0 12
execute at @s unless score #k289 snd matches 1 run function rlk:snd/f324
execute at @s unless score #k290 snd matches 1 run function rlk:snd/f325
kill @s
