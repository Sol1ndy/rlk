# off - tol <= forward <= off + len + tol and |side| <= half width + tol
scoreboard players operation #rdLo rd = @s rdHC
scoreboard players operation #rdLo rd -= @s rdHTol
scoreboard players operation #rdHi rd = @s rdHC
scoreboard players operation #rdHi rd += @s rdHA
scoreboard players operation #rdHi rd += @s rdHTol
scoreboard players operation #rdW rd = @s rdHB
scoreboard players operation #rdW rd += @s rdHTol
execute if score #rdFwd rd >= #rdLo rd if score #rdFwd rd <= #rdHi rd if score #rdAbsSide rd <= #rdW rd run scoreboard players set #rdHit rd 1
