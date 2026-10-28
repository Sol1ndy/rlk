# 3 b behind the body (then the back diagonals, then the sides) on walked-to safe ground; else in place
scoreboard players set #c2ok tmp 0
summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}
function rlk:cm/nj/v_try {a:180}
execute if score #c2ok tmp matches 0 run function rlk:cm/nj/v_try {a:140}
execute if score #c2ok tmp matches 0 run function rlk:cm/nj/v_try {a:-140}
execute if score #c2ok tmp matches 0 run function rlk:cm/nj/v_try {a:100}
execute if score #c2ok tmp matches 0 run function rlk:cm/nj/v_try {a:-100}
execute if score #c2ok tmp matches 1 run tp @s @e[tag=rlk_c2cur,limit=1]
kill @e[tag=rlk_c2cur]
scoreboard players set @s cmS 2
scoreboard players set @s cmT 12
# the rig stays hidden for this tick while it moves; it appears next tick, crouched, blade glinting
scoreboard players set @s cmAR 1
tag @s remove rlk_cmch
execute at @s run particle minecraft:large_smoke ~ ~1 ~ 0.35 0.6 0.35 0.02 24
execute at @s run particle minecraft:poof ~ ~1 ~ 0.4 0.6 0.4 0.03 16
execute at @s run particle minecraft:end_rod ~ ~1.6 ~ 0.1 0.1 0.1 0.02 3
execute at @s run playsound minecraft:entity.phantom.flap master @a ~ ~ ~ 1 1.4
execute at @s run playsound minecraft:block.note_block.bell master @a ~ ~ ~ 0.9 2
