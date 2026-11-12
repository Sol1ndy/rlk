# Travelling disk: centre at forward F = d0 + v*t on the axis, radius r + tol (rdHD).
scoreboard players operation #rdF rd = #rdRel rd
scoreboard players operation #rdF rd *= @s rdHB
scoreboard players operation #rdF rd /= #rdK1000 rd
scoreboard players operation #rdF rd += @s rdHA
scoreboard players operation #rdQ rd = #rdFwd rd
scoreboard players operation #rdQ rd -= #rdF rd
execute if score #rdQ rd matches ..-1 run scoreboard players operation #rdQ rd *= #rdNeg rd
execute if score #rdQ rd > @s rdHD run return 0
execute if score #rdAbsSide rd > @s rdHD run return 0
scoreboard players operation #rdQ rd *= #rdQ rd
scoreboard players operation #rdT rd = #rdAbsSide rd
scoreboard players operation #rdT rd *= #rdAbsSide rd
scoreboard players operation #rdQ rd += #rdT rd
scoreboard players operation #rdT rd = @s rdHD
scoreboard players operation #rdT rd *= @s rdHD
execute if score #rdQ rd <= #rdT rd run scoreboard players set #rdHit rd 1
