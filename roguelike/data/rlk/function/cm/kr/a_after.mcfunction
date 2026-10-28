scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches 1.. run return 0
execute if score @s cmN matches ..2 run return run function rlk:cm/kr/a_next
function rlk:cm/kr/a_rest_start
