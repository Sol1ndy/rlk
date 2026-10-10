scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
function rlk:cm/sh/turn
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/sh/bash {d:"shS"}
