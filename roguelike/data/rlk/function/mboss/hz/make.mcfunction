# In the caller's context (floor point, aim yaw). Summons the hazard marker, then resets the options.
# Refused while the boss is dying (#mbSt 2: a lethal true hit inside the module tick must not leave
# hazards behind lib_clear); #hzLast is then 0.
execute if score #mbSt mb matches 2 run scoreboard players set #hzLast mb 0
execute if score #mbSt mb matches 2 run function rlk:mboss/opts_reset
execute if score #mbSt mb matches 2 run return fail
scoreboard players set #mbHzOn mb 1
execute rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_hz","rlk_mb_aux","rlk_room","rlk_mb_hznew"]}
execute rotated ~ 0 as @e[tag=rlk_mb_hznew,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[tag=rlk_mb_hznew,limit=1] at @s rotated as @s run function rlk:mboss/hz/init
tag @e[tag=rlk_mb_hznew] remove rlk_mb_hznew
function rlk:mboss/opts_reset
