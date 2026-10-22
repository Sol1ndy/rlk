# @s = a free spawn point: basic 3 of the wave (wave 1: ranged, else 50 / 50).
tag @s remove rlk_mb_ap_cand
tag @s add rlk_mb_ap_cused
execute if score #apWave mb matches 1 run return run function rlk:boss/apep/org/mark {k:1,a:1}
function rlk:boss/apep/org/mark {k:1,a:-1}
