# @s = body: visible again: the registry scale and the torso click shield (shield:true).
execute if score #apHide mb matches 0 run return 0
scoreboard players set #apHide mb 0
function rlk:mboss/body_scale {s:2}
tag @s remove rlk_mb_noshield
