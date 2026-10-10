# Keep the last aimed yaw throughout the existing delayed shot.
function rlk:cm/cn/rig/aim
scoreboard players set @s cmS 2
scoreboard players operation @s cmT = #cmW_cnD tmp
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.12 ^1.30 run function rlk:cm/cn/shot
