# Travelling straight front: F = d0 + v*t; forward in [F - depth - tol, F + tol], |side| <= w + tol.
scoreboard players operation #rdF rd = #rdRel rd
scoreboard players operation #rdF rd *= @s rdHB
scoreboard players operation #rdF rd /= #rdK1000 rd
scoreboard players operation #rdF rd += @s rdHA
scoreboard players operation #rdHi rd = #rdF rd
scoreboard players operation #rdHi rd += @s rdHTol
scoreboard players operation #rdLo rd = #rdF rd
scoreboard players operation #rdLo rd -= @s rdHD
scoreboard players operation #rdLo rd -= @s rdHTol
scoreboard players operation #rdW rd = @s rdHC
scoreboard players operation #rdW rd += @s rdHTol
execute if score #rdFwd rd >= #rdLo rd if score #rdFwd rd <= #rdHi rd if score #rdAbsSide rd <= #rdW rd run scoreboard players set #rdHit rd 1
