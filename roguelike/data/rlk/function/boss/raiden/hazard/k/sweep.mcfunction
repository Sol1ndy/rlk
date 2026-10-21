# Travelling arc: front F = r0 + v*t; band [F - band - tol, F + tol]; |angle| <= half (half 180: whole ring).
scoreboard players operation #rdF rd = #rdRel rd
scoreboard players operation #rdF rd *= @s rdHB
scoreboard players operation #rdF rd /= #rdK1000 rd
scoreboard players operation #rdF rd += @s rdHA
scoreboard players operation #rdHi rd = #rdF rd
scoreboard players operation #rdHi rd += @s rdHTol
scoreboard players operation #rdHi rd *= #rdHi rd
execute if score #rdR2 rd > #rdHi rd run return 0
scoreboard players operation #rdLo rd = #rdF rd
scoreboard players operation #rdLo rd -= @s rdHC
scoreboard players operation #rdLo rd -= @s rdHTol
execute if score #rdLo rd matches ..-1 run scoreboard players set #rdLo rd 0
scoreboard players operation #rdLo rd *= #rdLo rd
# S3-F perf (review RD-P1): the front only moves outward, so once the body is behind the band this hazard can
# never reach it: it is spent (rdHHit = rdHMax) and `try` skips it until it expires; its cards fly on.
execute if score #rdR2 rd < #rdLo rd run return run scoreboard players operation @s rdHHit > @s rdHMax
execute if score @s rdHE matches ..-999 run return run scoreboard players set #rdHit rd 1
function rlk:boss/raiden/hazard/fs
scoreboard players operation #rdT rd = #rdFwd rd
scoreboard players operation #rdT rd *= @s rdHD
scoreboard players operation #rdT2 rd = #rdAbsSide rd
scoreboard players operation #rdT2 rd *= @s rdHE
scoreboard players operation #rdT rd -= #rdT2 rd
execute if score #rdT rd matches 0.. run scoreboard players set #rdHit rd 1
