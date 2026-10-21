# @s boss where it stands. Immune while rdBlink 1.. (combat/apply); relocates at rdBlink 6 (4 t later).
execute if score @s rdBlink matches 1.. run return 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdBlink 1
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/rig/play/t_blink_out
execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/rig/play/blink_out
execute at @s run function rlk:boss/raiden/fx/blink_out
