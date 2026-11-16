scoreboard players operation #dmg tmp /= #rd10 rd
scoreboard players add @s rdSgGm 1
scoreboard players add @s rdSgGp 1
execute at @s rotated as @s run function rlk:boss/raiden/fx/parry
execute unless score @s rdSgCt matches 1.. run function rlk:boss/raiden/rig/play/parry
# In-guard counter (B-04/05): 35 % on a parried hit, cooldown 60 t, only while it ends
# before the guard does (160).
execute if score @s rdSgCt matches 1.. run return 0
execute if score @s rdSgCcd matches 1.. run return 0
execute if score @s rdWpn matches 0 if score @s rdTime matches 112.. run return 0
execute if score @s rdTime matches 132.. run return 0
execute store result score #rdSgR rd run random value 0..99
execute if score #rdSgR rd matches ..34 at @s run function rlk:boss/raiden/sg/counter_start
