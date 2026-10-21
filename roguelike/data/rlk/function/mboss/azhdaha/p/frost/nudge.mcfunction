# @s = the centre, at it: 4 b away from a live field within 6 b; out of an orbit band (orbs at r 6.5 / 10.5, hr
# 1.3 about the orbit centre) in 0.5-b steps (<= 3 b).
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_fld,distance=..6] facing entity @e[type=minecraft:marker,tag=rlk_mb_az_fld,distance=..6,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-4
scoreboard players set #aq41N mb 0
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_orb,limit=1] if entity @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] at @s run function rlk:mboss/azhdaha/p/frost/nudge_o
