execute if entity @e[tag=rlk_body,distance=..3.0] run function rlk:cm/kr/b_dmg
execute rotated 0 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 45 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 90 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 135 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 180 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 225 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 270 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 315 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
particle minecraft:electric_spark ~ ~1 ~ 1.4 0.3 1.4 0.1 40
playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 1 0.8
playsound minecraft:entity.lightning_bolt.impact master @a ~ ~ ~ 0.6 1.6
scoreboard players set @s cmS 5
scoreboard players set @s cmT 12
scoreboard players set @s cmCd2 100
execute if score @s cmCd matches ..15 run scoreboard players set @s cmCd 16
tag @s remove rlk_cmch
