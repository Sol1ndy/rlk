# One growth tick of every live frost ring (azT = ticks since the strike); the chain runs while one lives.
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr] run scoreboard players add @s azT 1
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={azT=1}] run function rlk:mboss/hz/resize {r:22,r0:8,w:0}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={azT=2}] run function rlk:mboss/hz/resize {r:30,r0:15,w:0}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={azT=3}] run function rlk:mboss/hz/resize {r:38,r0:22,w:0}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={azT=4}] run function rlk:mboss/hz/resize {r:45,r0:30,w:0}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={azT=5}] run function rlk:mboss/hz/resize {r:52,r0:38,w:0}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={azT=6}] run function rlk:mboss/hz/resize {r:60,r0:45,w:0}
tag @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={azT=6..}] remove rlk_mb_az_xcr
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_xcr,limit=1] run scoreboard players set #azAftF mb 44
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_xcr,limit=1] run scoreboard players set #azAftD mb 1
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_xcr,limit=1] run function rlk:mboss/azhdaha/aft/new
