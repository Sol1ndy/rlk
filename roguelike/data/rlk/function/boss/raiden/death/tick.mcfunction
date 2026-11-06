function rlk:boss/raiden/line/tick
scoreboard players add @s rdDeathTime 1
data merge entity @s {Motion:[0d,0d,0d],Health:1024f,Fire:-1s}
execute if score @s rdDeathTime matches 48.. run return run function rlk:boss/raiden/death/finish
function rlk:boss/raiden/rig/tick
