# 6 b straight away from the body (then the back diagonals, the sides) on walked safe ground; at least 4 b
scoreboard players set #c2ok tmp 0
summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}
function rlk:cm/cc/b_try {a:180}
execute if score #c2ok tmp matches 0 run function rlk:cm/cc/b_try {a:135}
execute if score #c2ok tmp matches 0 run function rlk:cm/cc/b_try {a:-135}
execute if score #c2ok tmp matches 0 run function rlk:cm/cc/b_try {a:90}
execute if score #c2ok tmp matches 0 run function rlk:cm/cc/b_try {a:-90}
execute if score #c2ok tmp matches 1 run function rlk:cm/cc/b_land
kill @e[tag=rlk_c2cur]
execute if score #c2ok tmp matches 0 run function rlk:cm/cc/b_fail
