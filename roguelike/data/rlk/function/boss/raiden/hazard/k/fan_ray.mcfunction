scoreboard players operation #rdRayF rd = #rdFwd rd
scoreboard players operation #rdRayF rd *= #rdCos rd
scoreboard players operation #rdT rd = #rdSide rd
scoreboard players operation #rdT rd *= #rdSin rd
scoreboard players operation #rdRayF rd += #rdT rd
scoreboard players operation #rdRayF rd /= #rdK1000 rd
execute if score #rdRayF rd matches ..-1 run return 0
execute if score #rdRayF rd > @s rdHA run return 0
scoreboard players operation #rdRayS rd = #rdSide rd
scoreboard players operation #rdRayS rd *= #rdCos rd
scoreboard players operation #rdT rd = #rdFwd rd
scoreboard players operation #rdT rd *= #rdSin rd
scoreboard players operation #rdRayS rd -= #rdT rd
scoreboard players operation #rdRayS rd /= #rdK1000 rd
execute if score #rdRayS rd matches ..-1 run scoreboard players operation #rdRayS rd *= #rdNeg rd
execute if score #rdRayS rd <= @s rdHB run scoreboard players set #rdHit rd 1
