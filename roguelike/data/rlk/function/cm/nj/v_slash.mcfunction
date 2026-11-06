# a short lunge (up to 1.5 b of walked safe ground toward the body), then the cut
summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #wN tmp 3
execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/nj/lib/walk
execute if score #wK tmp matches 1.. run tp @s @e[tag=rlk_c2cur,limit=1]
kill @e[tag=rlk_c2cur]
execute at @s if entity @e[tag=rlk_body,distance=..2.3] run function rlk:cm/nj/v_dmg
execute at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ^ ^1.1 ^1.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute at @s run playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 1 1.4
scoreboard players add @s cmN 1
scoreboard players set @s cmS 3
scoreboard players set @s cmT 5
