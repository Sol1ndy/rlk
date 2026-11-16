# The swallow (pred_swallow 24 t: rear 0-6, scoop 6-12, the basic removed at 12): the basic is held (its slot freed).
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,tag=!rlk_mb_ap_prey,sort=nearest,limit=1] run function rlk:boss/apep/org/pred/hold
execute at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_ap_prey,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
scoreboard players set @s apS 2
scoreboard players set @s apT 0
function rlk:boss/apep/om/pred/play/pred_swallow
