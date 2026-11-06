# @s = a ring circle (rotated to its bearing): r 9-16 from the centre (12.5-16 while orbs live: off the orbit bands),
# 4 b away from a live field within 6 b, kept <= 24 b.
execute store result storage rlk:mboss az.p42.d double 0.1 run random value 90..160
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_orb,limit=1] store result storage rlk:mboss az.p42.d double 0.1 run random value 125..160
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated as @s run function rlk:boss/azhdaha/p/bolt/mv with storage rlk:mboss az.p42
execute at @s if entity @e[type=minecraft:marker,tag=rlk_mb_az_fld,distance=..6] facing entity @e[type=minecraft:marker,tag=rlk_mb_az_fld,distance=..6,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-4
function rlk:boss/azhdaha/u/clamp_r {r:24}
