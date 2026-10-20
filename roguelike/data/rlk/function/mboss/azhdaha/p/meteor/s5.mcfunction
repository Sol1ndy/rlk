# Small meteor 5 (hit t94): its target, then the hazard + the air halo + the prop high above it.
execute store result storage rlk:mboss az.p32.r.a int 1 run random value 0..359
execute store result storage rlk:mboss az.p32.r.d int 1 run random value 6..14
data modify storage rlk:mboss az.p32.r.t set value "rlk_mb_az_p32m5"
function rlk:mboss/azhdaha/xl/u/rnd with storage rlk:mboss az.p32.r
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_p32
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] remove rlk_mb_az_xnt
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p32m5,limit=1] run function rlk:mboss/azhdaha/xl/u/clear_met
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32m5,limit=1] run function rlk:mboss/azhdaha/p/meteor/s5_hz
