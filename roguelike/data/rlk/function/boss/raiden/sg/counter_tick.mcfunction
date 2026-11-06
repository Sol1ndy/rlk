# Pattern 9, every guard tick while a counter runs (c = rdSgCt - 2; c0 = the first boss tick after the parry).
scoreboard players add @s rdSgCt 1
execute if score @s rdSgCt matches 2 run function rlk:boss/raiden/sg/counter_c0
execute if score @s rdSgCk matches 0 if score @s rdSgCt matches 14 at @s run function rlk:boss/raiden/sg/counter_s12
execute if score @s rdSgCk matches 0 if score @s rdSgCt matches 30 at @s run function rlk:boss/raiden/sg/counter_s28
execute if score @s rdSgCk matches 0 if score @s rdSgCt matches 48.. run function rlk:boss/raiden/sg/counter_end
execute if score @s rdSgCk matches 1 if score @s rdSgCt matches 10 at @s rotated as @s run execute positioned ~ ~1.6 ~ run execute positioned ^ ^ ^0.8 run function rlk:boss/raiden/fx/star
execute if score @s rdSgCk matches 1 if score @s rdSgCt matches 28.. run function rlk:boss/raiden/sg/counter_end
