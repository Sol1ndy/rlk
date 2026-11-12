execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_plkb_source"]}
execute if score #mbKBDir mb matches 0 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 run tp @e[tag=rlk_plkb_source,limit=1] ~ ~ ~ ~ 0
execute if score #mbKBDir mb matches 1 at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_plkb_source,limit=1] ~ ~ ~ ~ 0
