# Stand-in anchor blade_mid (@s = body, at its feet): the rlk_hr_anchor marker at ^0.45 ^1.2 ^0.95.
execute unless entity @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_anchor"]}
execute at @s rotated as @s rotated ~ 0 positioned ^0.45 ^1.2 ^0.95 run tp @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] ~ ~ ~ ~ 0
