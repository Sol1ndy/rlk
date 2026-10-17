scoreboard players set #pjKeep mb 0
function rlk:mboss/d/pj_end
execute if score #pjKeep mb matches 1 run return run function rlk:mboss/pj/release
kill @s
