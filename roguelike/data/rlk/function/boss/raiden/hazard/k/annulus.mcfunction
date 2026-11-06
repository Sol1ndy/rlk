# rmin - tol <= d <= r + tol and |angle| <= half  <=>  fwd*sin(half) - |side|*cos(half) >= 0 (any half 0..180).
execute if score #rdR2 rd > @s rdHE run return 0
execute if score #rdR2 rd < @s rdHF run return 0
scoreboard players operation #rdT rd = #rdFwd rd
scoreboard players operation #rdT rd *= @s rdHC
scoreboard players operation #rdT2 rd = #rdAbsSide rd
scoreboard players operation #rdT2 rd *= @s rdHD
scoreboard players operation #rdT rd -= #rdT2 rd
execute if score #rdT rd matches 0.. run scoreboard players set #rdHit rd 1
