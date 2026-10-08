execute unless data storage rlk:room q[0] run return 0
execute store result score #bx0 tmp run data get storage rlk:room q[0].x0
execute store result score #bx1 tmp run data get storage rlk:room q[0].x1
execute store result score #bz0 tmp run data get storage rlk:room q[0].z0
execute store result score #bz1 tmp run data get storage rlk:room q[0].z1
scoreboard players operation #bx0 tmp > #ax0 tmp
scoreboard players operation #bx1 tmp < #ax1 tmp
scoreboard players operation #bz0 tmp > #az0 tmp
scoreboard players operation #bz1 tmp < #az1 tmp
execute store result storage rlk:room w.x0 int 1 run scoreboard players get #bx0 tmp
execute store result storage rlk:room w.x1 int 1 run scoreboard players get #bx1 tmp
execute store result storage rlk:room w.z0 int 1 run scoreboard players get #bz0 tmp
execute store result storage rlk:room w.z1 int 1 run scoreboard players get #bz1 tmp
execute if score #bx0 tmp <= #bx1 tmp if score #bz0 tmp <= #bz1 tmp run function rlk:room/wave_fill with storage rlk:room w
data remove storage rlk:room q[0]
function rlk:room/wave_cells
