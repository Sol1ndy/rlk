scoreboard players operation #rdRayF rd = #rdFwd rd
scoreboard players operation #rdRayF rd *= #rdCos rd
scoreboard players operation #rdT rd = #rdSide rd
scoreboard players operation #rdT rd *= #rdSin rd
scoreboard players operation #rdRayF rd += #rdT rd
scoreboard players operation #rdRayF rd /= #rdScale rd
execute unless score #rdRayF rd matches 0..18000 run return 0
scoreboard players operation #rdRayS rd = #rdSide rd
scoreboard players operation #rdRayS rd *= #rdCos rd
scoreboard players operation #rdT rd = #rdFwd rd
scoreboard players operation #rdT rd *= #rdSin rd
scoreboard players operation #rdRayS rd -= #rdT rd
scoreboard players operation #rdRayS rd /= #rdScale rd
execute if score #rdRayS rd matches -450..450 run scoreboard players set #rdHit rd 1
