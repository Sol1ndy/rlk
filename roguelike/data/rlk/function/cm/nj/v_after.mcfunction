scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches 1.. run return 0
execute if score @s cmN matches 2.. run return run function rlk:cm/nj/tired_start
function rlk:cm/nj/idle
scoreboard players set @s cmCd 14
