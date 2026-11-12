# yaw toward the body; while ramming, along the locked ram line
execute if score @s cmS matches 2 rotated as @s rotated ~ 0 as @e[tag=rlk_ci_this] run tp @s ~ ~ ~ ~ 0
execute unless score @s cmS matches 2 facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_ci_this] run tp @s ~ ~ ~ ~ 0
