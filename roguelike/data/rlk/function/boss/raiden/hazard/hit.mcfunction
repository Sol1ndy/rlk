# @s = hazard at its origin. Body feet (rlk_body) relative to the origin; R2 only for radial kinds.
scoreboard players set #rdHit rd 0
execute unless entity @e[tag=rlk_body,distance=..46,limit=1] run return 0
execute store result score #rdDX rd run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #rdDZ rd run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute store result score #rdOX rd run data get entity @s Pos[0] 1000
execute store result score #rdOZ rd run data get entity @s Pos[2] 1000
scoreboard players operation #rdDX rd -= #rdOX rd
scoreboard players operation #rdDZ rd -= #rdOZ rd
execute if score @s rdHK matches 1..2 run function rlk:boss/raiden/hazard/r2
execute if score @s rdHK matches 5 run function rlk:boss/raiden/hazard/r2
execute if score @s rdHK matches 8..10 run function rlk:boss/raiden/hazard/r2
execute if score @s rdHK matches 10 run return run function rlk:boss/raiden/hazard/k/safe_dome
execute store result score #rdDY rd run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000
execute store result score #rdOY rd run data get entity @s Pos[1] 1000
scoreboard players operation #rdDY rd -= #rdOY rd
execute unless score #rdDY rd matches -500..3500 run return 0
execute if entity @s[tag=rlk_rd_jump] unless score #rdDY rd matches -500..750 run return 0
execute unless score @s rdHK matches 1 unless score @s rdHK matches 5 unless score @s rdHK matches 8..9 run function rlk:boss/raiden/hazard/fs
execute if score @s rdHK matches 1 run function rlk:boss/raiden/hazard/k/disk
execute if score @s rdHK matches 2 run function rlk:boss/raiden/hazard/k/annulus
execute if score @s rdHK matches 3 run function rlk:boss/raiden/hazard/k/rect
execute if score @s rdHK matches 5 run function rlk:boss/raiden/hazard/k/sweep
execute if score @s rdHK matches 6 run function rlk:boss/raiden/hazard/k/slab
execute if score @s rdHK matches 7 run function rlk:boss/raiden/hazard/k/orb
execute if score @s rdHK matches 8 run function rlk:boss/raiden/hazard/k/follow
execute if score @s rdHK matches 9 run function rlk:boss/raiden/hazard/k/field
execute if score @s rdHK matches 11 run function rlk:boss/raiden/hazard/k/fan
execute if score @s rdHK matches 4 run function rlk:boss/raiden/hazard/k/rect
execute if score #rdHit rd matches 1 run function rlk:boss/raiden/hazard/land
