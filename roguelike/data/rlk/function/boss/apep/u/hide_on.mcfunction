# @s = body: hidden (burrowed / parked): scale 0.1, no click shield (cm.md 5.5, FN-13).
execute if score #apHide mb matches 1 run return 0
scoreboard players set #apHide mb 1
function rlk:mboss/body_scale {s:0.1}
tag @s add rlk_mb_noshield
