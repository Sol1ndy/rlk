# toward the ring point (r 4, 1.2 b up; r 2.5 when that is inside a block) at 0.4 b/tick, never into a block
scoreboard players add @s c2eA 6
execute if score #eStep tmp matches 2 run scoreboard players add @s c2eA 6
execute if score @s c2eA matches 360.. run scoreboard players remove @s c2eA 360
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 1 run scoreboard players get @s c2eA
execute positioned as @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.2 ^4 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~
execute at @e[tag=rlk_cmrot,limit=1] unless block ~ ~ ~ #rlk:dash_pass run return run function rlk:cm/ci/orbit_near
execute at @e[tag=rlk_cmrot,limit=1] unless block ~ ~0.5 ~ #rlk:dash_pass run return run function rlk:cm/ci/orbit_near
function rlk:cm/ci/orbit_go
