# Travelling straight front: F = d0 + v*t; forward in [F - depth - tol, F + tol], |side| <= w + tol.
# S3 perf: the forward test comes first (hazard/hit skips fs for slabs), so the ticks while the front is away from
# the body cost no side projection.
scoreboard players operation #rdF rd = #rdRel rd
scoreboard players operation #rdF rd *= @s rdHB
scoreboard players operation #rdF rd /= #rdK1000 rd
scoreboard players operation #rdF rd += @s rdHA
scoreboard players operation #rdHi rd = #rdF rd
scoreboard players operation #rdHi rd += @s rdHTol
scoreboard players operation #rdLo rd = #rdF rd
scoreboard players operation #rdLo rd -= @s rdHD
scoreboard players operation #rdLo rd -= @s rdHTol
scoreboard players operation #rdFwd rd = #rdDX rd
scoreboard players operation #rdFwd rd *= @s rdFX
scoreboard players operation #rdT rd = #rdDZ rd
scoreboard players operation #rdT rd *= @s rdFZ
scoreboard players operation #rdFwd rd += #rdT rd
scoreboard players operation #rdFwd rd /= #rdK1000 rd
execute if score #rdFwd rd < #rdLo rd run return 0
execute if score #rdFwd rd > #rdHi rd run return 0
scoreboard players operation #rdSide rd = #rdDX rd
scoreboard players operation #rdSide rd *= @s rdFZ
scoreboard players operation #rdT rd = #rdDZ rd
scoreboard players operation #rdT rd *= @s rdFX
scoreboard players operation #rdSide rd -= #rdT rd
scoreboard players operation #rdSide rd /= #rdK1000 rd
scoreboard players operation #rdAbsSide rd = #rdSide rd
scoreboard players set #rdNeg rd -1
execute if score #rdAbsSide rd matches ..-1 run scoreboard players operation #rdAbsSide rd *= #rdNeg rd
scoreboard players operation #rdW rd = @s rdHC
scoreboard players operation #rdW rd += @s rdHTol
execute if score #rdAbsSide rd <= #rdW rd run scoreboard players set #rdHit rd 1
