# Project onto the frozen forward and left axes (milliblocks).
scoreboard players operation #rdFwd rd = #rdDX rd
scoreboard players operation #rdFwd rd *= @s rdFX
scoreboard players operation #rdT rd = #rdDZ rd
scoreboard players operation #rdT rd *= @s rdFZ
scoreboard players operation #rdFwd rd += #rdT rd
scoreboard players operation #rdFwd rd /= #rdK1000 rd
scoreboard players operation #rdSide rd = #rdDX rd
scoreboard players operation #rdSide rd *= @s rdFZ
scoreboard players operation #rdT rd = #rdDZ rd
scoreboard players operation #rdT rd *= @s rdFX
scoreboard players operation #rdSide rd -= #rdT rd
scoreboard players operation #rdSide rd /= #rdK1000 rd
scoreboard players operation #rdAbsSide rd = #rdSide rd
scoreboard players set #rdNeg rd -1
execute if score #rdAbsSide rd matches ..-1 run scoreboard players operation #rdAbsSide rd *= #rdNeg rd
