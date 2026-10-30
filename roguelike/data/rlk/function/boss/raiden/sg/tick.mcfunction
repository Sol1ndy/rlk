# core tick, phase 0, as the boss at its feet.
execute if score @s rdSgRearT matches 1.. run scoreboard players remove @s rdSgRearT 1
execute if score @s rdSgRearCD matches 1.. run scoreboard players remove @s rdSgRearCD 1
execute if score @s rdSgCcd matches 1.. run scoreboard players remove @s rdSgCcd 1
execute if score @s rdSgFx matches 1.. run function rlk:boss/raiden/sg/fx_tick
