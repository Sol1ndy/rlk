scoreboard players operation #coef tmp = #bowAim tmp
function rlk:char/bow/calc
scoreboard players operation #aEl tmp = @s infuse
execute unless score #aEl tmp matches 0..8 run scoreboard players set #aEl tmp 0
scoreboard players set #aKind tmp 2
