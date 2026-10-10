# Use body feet, not the displaced third-person spectator camera.
scoreboard players set #rdHit rd 0
execute unless entity @e[tag=rlk_body,distance=..28,limit=1] run return 0
execute store result score #rdDY rd run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000
execute store result score #rdOY rd run data get entity @s Pos[1] 1000
scoreboard players operation #rdDY rd -= #rdOY rd
execute unless score #rdDY rd matches -500..3500 run return 0
execute if score @s rdShape matches 11 unless score #rdDY rd matches -500..750 run return 0
execute store result score #rdDX rd run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #rdDZ rd run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute store result score #rdOX rd run data get entity @s Pos[0] 1000
execute store result score #rdOZ rd run data get entity @s Pos[2] 1000
scoreboard players operation #rdDX rd -= #rdOX rd
scoreboard players operation #rdDZ rd -= #rdOZ rd
scoreboard players set #rdScale rd 1000
# Distance squared stays below 784 million after the 28-block broad phase.
scoreboard players operation #rdR2 rd = #rdDX rd
scoreboard players operation #rdR2 rd *= #rdDX rd
scoreboard players operation #rdT rd = #rdDZ rd
scoreboard players operation #rdT rd *= #rdDZ rd
scoreboard players operation #rdR2 rd += #rdT rd
# Project onto frozen local forward and left axes (milliblocks).
scoreboard players operation #rdFwd rd = #rdDX rd
scoreboard players operation #rdFwd rd *= @s rdFX
scoreboard players operation #rdT rd = #rdDZ rd
scoreboard players operation #rdT rd *= @s rdFZ
scoreboard players operation #rdFwd rd += #rdT rd
scoreboard players operation #rdFwd rd /= #rdScale rd
scoreboard players operation #rdSide rd = #rdDX rd
scoreboard players operation #rdSide rd *= @s rdFZ
scoreboard players operation #rdT rd = #rdDZ rd
scoreboard players operation #rdT rd *= @s rdFX
scoreboard players operation #rdSide rd -= #rdT rd
scoreboard players operation #rdSide rd /= #rdScale rd
scoreboard players operation #rdAbsSide rd = #rdSide rd
scoreboard players set #rdNeg rd -1
execute if score #rdAbsSide rd matches ..-1 run scoreboard players operation #rdAbsSide rd *= #rdNeg rd
execute if score @s rdShape matches 1 run function rlk:boss/raiden/hazard/hit/s1
execute if score @s rdShape matches 2 run function rlk:boss/raiden/hazard/hit/s2
execute if score @s rdShape matches 3 run function rlk:boss/raiden/hazard/hit/s3
execute if score @s rdShape matches 4 run function rlk:boss/raiden/hazard/hit/s4
execute if score @s rdShape matches 5 run function rlk:boss/raiden/hazard/hit/s5
execute if score @s rdShape matches 6 run function rlk:boss/raiden/hazard/hit/s6
execute if score @s rdShape matches 7 run function rlk:boss/raiden/hazard/hit/s7
execute if score @s rdShape matches 8 run function rlk:boss/raiden/hazard/hit/s8
execute if score @s rdShape matches 9 run function rlk:boss/raiden/hazard/hit/s9
execute if score @s rdShape matches 10 run function rlk:boss/raiden/hazard/hit/s10
execute if score @s rdShape matches 11 run function rlk:boss/raiden/hazard/hit/s11
execute if score @s rdShape matches 12 run function rlk:boss/raiden/hazard/hit/s12
execute if score @s rdShape matches 13 run function rlk:boss/raiden/hazard/hit/s13
execute unless score #rdHit rd matches 1 run return 0
scoreboard players set @s rdHHit 1
scoreboard players operation #cmDmg tmp = @s rdDamage
scoreboard players operation #cmLv tmp = @s mlv
scoreboard players set #cmEl tmp 3
function rlk:boss/raiden/hurt
