execute as @e[tag=rlk_pk_el,distance=..0.47,limit=1,sort=nearest] run return run function rlk:lvup/ray_hit
scoreboard players add #pkRay tmp 1
execute if score #pkRay tmp matches 40.. run return 0
execute positioned ^ ^ ^0.22 run function rlk:lvup/ray
