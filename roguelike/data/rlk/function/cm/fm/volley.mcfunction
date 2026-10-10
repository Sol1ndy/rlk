scoreboard players set #hold tmp 1
function rlk:cm/fm/hold
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/fm/shot
