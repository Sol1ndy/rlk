# @s = a fire field hazard near the branded player: extended by its base life.
execute as @s run function rlk:boss/azhdaha/fld/refresh {n:160}
scoreboard players set #aq33X mb 1
execute at @s run function rlk:boss/azhdaha/fx/p/fire_field {r:45}
