# Armored sector radius12, 140 degrees (radius plus analytic yaw-sector bounds).
execute unless score #rdR2 rd matches ..144000000 run return 0
execute unless score #rdFwd rd matches 0.. run return 0
scoreboard players operation #rdLimit rd = #rdFwd rd
scoreboard players set #rdTan rd 2747
scoreboard players operation #rdLimit rd *= #rdTan rd
scoreboard players operation #rdLimit rd /= #rdScale rd
execute if score #rdAbsSide rd <= #rdLimit rd run scoreboard players set #rdHit rd 1
