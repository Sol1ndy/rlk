# @s = a free spawn point: basic 1 of the wave (wave 1: melee, else 50 / 50).
tag @s remove rlk_mb_ap_cand
tag @s add rlk_mb_ap_cused
execute if score #apWave mb matches 1 run return run function rlk:boss/apep/org/mark {k:1,a:0}
function rlk:boss/apep/org/mark {k:1,a:-1}
