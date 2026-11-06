execute if entity @e[tag=rlk_body,distance=..3.0] run function rlk:cm/pc/sp_dmg
execute rotated 0 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 45 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 90 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 135 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 180 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 225 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 270 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute rotated 315 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
playsound minecraft:entity.breeze.shoot master @a ~ ~ ~ 1 0.7
playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 1 0.6
scoreboard players set @s cmS 6
scoreboard players set @s cmT 8
tag @s remove rlk_cmch
