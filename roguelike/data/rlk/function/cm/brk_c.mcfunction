execute unless data storage rlk:cm cs[0] run return 0
execute store result score #ix0 tmp run data get storage rlk:cm cs[0].ix0
execute store result score #ix1 tmp run data get storage rlk:cm cs[0].ix1
execute store result score #iz0 tmp run data get storage rlk:cm cs[0].iz0
execute store result score #iz1 tmp run data get storage rlk:cm cs[0].iz1
scoreboard players operation #fx0 tmp = #bx tmp
scoreboard players operation #fx0 tmp -= #br tmp
scoreboard players operation #fx0 tmp > #ix0 tmp
scoreboard players operation #fx1 tmp = #bx tmp
scoreboard players operation #fx1 tmp += #br tmp
scoreboard players operation #fx1 tmp < #ix1 tmp
scoreboard players operation #fz0 tmp = #bz tmp
scoreboard players operation #fz0 tmp -= #br tmp
scoreboard players operation #fz0 tmp > #iz0 tmp
scoreboard players operation #fz1 tmp = #bz tmp
scoreboard players operation #fz1 tmp += #br tmp
scoreboard players operation #fz1 tmp < #iz1 tmp
execute if score #fx0 tmp <= #fx1 tmp if score #fz0 tmp <= #fz1 tmp run function rlk:cm/brk_go
data remove storage rlk:cm cs[0]
function rlk:cm/brk_c
