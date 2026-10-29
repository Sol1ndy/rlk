# displays to the brain; yaw toward the body, or the locked attack yaw cmYaw while rlk_c2_fix
execute if entity @s[tag=rlk_c2_fix] store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute if entity @s[tag=rlk_c2_fix] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 as @e[tag=rlk_cs_this] run tp @s ~ ~ ~ ~ 0
execute unless entity @s[tag=rlk_c2_fix] facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_cs_this] run tp @s ~ ~ ~ ~ 0
