# beside the body: walk 2 b out from the body's feet (sides, back diagonals, front diagonals, behind it), at least
# 1.5 b of walked safe ground; none -> reform where it scattered. The walk starts at the body, so never behind a wall.
scoreboard players set #c2ok tmp 0
summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}
function rlk:cm/pc/r_try {a:90}
execute if score #c2ok tmp matches 0 run function rlk:cm/pc/r_try {a:-90}
execute if score #c2ok tmp matches 0 run function rlk:cm/pc/r_try {a:135}
execute if score #c2ok tmp matches 0 run function rlk:cm/pc/r_try {a:-135}
execute if score #c2ok tmp matches 0 run function rlk:cm/pc/r_try {a:45}
execute if score #c2ok tmp matches 0 run function rlk:cm/pc/r_try {a:-45}
execute if score #c2ok tmp matches 0 run function rlk:cm/pc/r_try {a:180}
execute if score #c2ok tmp matches 1 run tp @s @e[tag=rlk_c2cur,limit=1]
kill @e[tag=rlk_c2cur]
scoreboard players set @s cmS 2
scoreboard players set @s cmT 10
execute at @s run playsound minecraft:block.amethyst_block.resonate master @a ~ ~ ~ 1 1.3
execute at @s run playsound minecraft:block.beacon.activate master @a ~ ~ ~ 0.6 1.8
