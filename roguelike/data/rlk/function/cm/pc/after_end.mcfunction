scoreboard players add @s cmN 1
execute if score @s cmN matches 2.. run return run function rlk:cm/pc/oh_start
function rlk:cm/pc/idle
scoreboard players set @s cmCd 16
