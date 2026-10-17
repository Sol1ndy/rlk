# In the caller's context (floor point, aim yaw). Summons the hazard marker, then resets the options.
execute rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_hz","rlk_mb_aux","rlk_room","rlk_mb_hznew"]}
execute rotated ~ 0 as @e[tag=rlk_mb_hznew,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[tag=rlk_mb_hznew,limit=1] at @s rotated as @s run function rlk:mboss/hz/init
tag @e[tag=rlk_mb_hznew] remove rlk_mb_hznew
function rlk:mboss/opts_reset
