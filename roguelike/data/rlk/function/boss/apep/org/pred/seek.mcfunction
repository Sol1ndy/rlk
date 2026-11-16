# Swimming at 0.15 b/t to the nearest basic; at <= 1.5 b it swallows it.
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,tag=!rlk_mb_ap_prey,sort=nearest,limit=1] run return run function rlk:boss/apep/org/pred/circle_go
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,tag=!rlk_mb_ap_prey,distance=..1.5] run return run function rlk:boss/apep/org/pred/swallow_go
execute facing entity @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,tag=!rlk_mb_ap_prey,sort=nearest,limit=1] feet run function rlk:mboss/mv/step_flat {spd:0.15}
function rlk:boss/apep/org/basic/push_in
function rlk:boss/apep/om/face
function rlk:boss/apep/org/pred/swim_snd
