# Core tick, as the boss, while rdBlink 1.. . The release timing: relocation + reform art at 4, the rig fades
# back in from 6 (unless a pattern clip already showed it), over at 10 (10 t immune).
execute unless score @s rdBlink matches 1.. run return 0
execute if score @s rdBlink matches 4 run function rlk:boss/raiden/movement/blink_land
execute if score @s rdBlink matches 6 if score @s rdRigS matches 2 unless score @s rdRigT matches -1 run function rlk:boss/raiden/movement/show
scoreboard players add @s rdBlink 1
execute if score @s rdBlink matches 10..19 run scoreboard players set @s rdBlink 0
execute if score @s rdBlink matches 30.. run scoreboard players set @s rdBlink 0
