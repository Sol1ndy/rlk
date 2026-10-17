# @s = new hazard marker, at/rotated as @s. Scores from #hz* (tenths -> milliblocks).
scoreboard players operation @s mbHzK = #hzK mb
scoreboard players operation @s mbHzW = #hzW mb
scoreboard players operation @s mbHzD = #hzD mb
scoreboard players operation @s mbHzA = #hzAct mb
scoreboard players operation @s mbHzE = #mbEl mb
execute if score #hzEl mb matches 0.. run scoreboard players operation @s mbHzE = #hzEl mb
scoreboard players operation @s mbHzB = #hzKB mb
scoreboard players operation @s mbHzKD = #hzKBDir mb
execute if score @s mbHzK matches 4 if score #hzKBDir mb matches 0 run scoreboard players set @s mbHzKD 1
scoreboard players operation @s mbHzS = #hzSfx mb
scoreboard players operation @s mbHzV = #hzVis mb
scoreboard players operation @s mbHzCol = @s mbHzE
execute if score #hzCol mb matches 0.. run scoreboard players operation @s mbHzCol = #hzCol mb
execute if score #hzQuiet mb matches 1 run tag @s add rlk_mb_hzq
execute if score @s mbHzW matches ..0 run scoreboard players set @s mbHzW 1
execute if score @s mbHzA matches ..0 run scoreboard players set @s mbHzA 1
scoreboard players set @s mbHzT -1
scoreboard players set @s mbHzHit 0
scoreboard players operation @s mbHzL = @s mbHzW
scoreboard players operation @s mbHzL += @s mbHzA
scoreboard players operation @s mbHzL += #hzLinger mb
scoreboard players add #hzId mb 1
scoreboard players operation @s mbHzI = #hzId mb
scoreboard players operation #hzLast mb = #hzId mb
scoreboard players operation @s mbHzY0 = #hzY0 mb
scoreboard players operation @s mbHzY0 *= #c100 mb
scoreboard players operation @s mbHzY1 = #hzY1 mb
scoreboard players operation @s mbHzY1 *= #c100 mb
scoreboard players operation @s mbHzR = #hzR mb
scoreboard players operation @s mbHzR *= #c100 mb
scoreboard players operation @s mbHzR0 = #hzR0 mb
scoreboard players operation @s mbHzR0 *= #c100 mb
scoreboard players set @s mbHzAng 180
scoreboard players set @s mbHzC 0
execute if score @s mbHzK matches 3 run function rlk:mboss/hz/init_sector
execute if score @s mbHzK matches 4 run function rlk:mboss/hz/init_line
# Squared bounds with a 0.3-block body pad: outer grows, inner (safe hole) shrinks.
scoreboard players operation #t mb = @s mbHzR
scoreboard players add #t mb 300
scoreboard players operation @s mbHzRR = #t mb
scoreboard players operation @s mbHzRR *= #t mb
scoreboard players operation #t mb = @s mbHzR0
scoreboard players remove #t mb 300
execute if score #t mb matches ..-1 run scoreboard players set #t mb 0
scoreboard players operation @s mbHzRI = #t mb
scoreboard players operation @s mbHzRI *= #t mb
# full: the safe circle is exact (body centre inside = safe).
execute if score @s mbHzK matches 5 run scoreboard players operation @s mbHzRI = @s mbHzR0
execute if score @s mbHzK matches 5 run scoreboard players operation @s mbHzRI *= @s mbHzR0
# Local forward axis x1000 from a temporary marker (exact, no trigonometry at runtime).
execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_hzax"]}
execute store result score #ox mb run data get entity @s Pos[0] 1000
execute store result score #oz mb run data get entity @s Pos[2] 1000
execute store result score @s mbHzFX run data get entity @e[tag=rlk_mb_hzax,limit=1] Pos[0] 1000
execute store result score @s mbHzFZ run data get entity @e[tag=rlk_mb_hzax,limit=1] Pos[2] 1000
scoreboard players operation @s mbHzFX -= #ox mb
scoreboard players operation @s mbHzFZ -= #oz mb
kill @e[tag=rlk_mb_hzax]
function rlk:mboss/hz/init_draw
execute if score @s mbHzV matches 1.. run scoreboard players set #hzEv mb 0
execute if score @s mbHzV matches 1.. run function rlk:mboss/d/hz_vis
