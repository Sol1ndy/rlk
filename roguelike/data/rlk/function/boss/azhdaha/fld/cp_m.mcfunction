# Macro {d}: at a clear point; a field centre (rlk_mb_az_fnew) within d is pushed out to d.
$execute as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,distance=..$(d),limit=1] at @s positioned ~0.01 ~ ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_fcp"]}
$execute as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,distance=..$(d),limit=1] facing entity @e[type=minecraft:marker,tag=rlk_mb_az_fcp,limit=1] feet rotated ~ 0 positioned ^ ^ ^$(d) run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_mb_az_fcp]
