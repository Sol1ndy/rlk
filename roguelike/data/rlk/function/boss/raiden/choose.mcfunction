execute if score @s rdPhase matches 0 store result score @s rdPat run random value 1..7
execute if score @s rdPhase matches 2 store result score @s rdPat run random value 11..18
execute if score @s rdPat = @s rdPrev run scoreboard players add @s rdPat 1
execute if score @s rdPhase matches 0 if score @s rdPat matches 8 run scoreboard players set @s rdPat 1
execute if score @s rdPhase matches 2 if score @s rdPat matches 19 run scoreboard players set @s rdPat 11
scoreboard players add @s rdTurns 1
scoreboard players operation #rdTurn rd = @s rdTurns
scoreboard players operation #rdTurn rd %= #rd4 rd
# At most one ultimate in each transformation, guaranteed by the fourth move.
execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 1 if score @s rdPat matches 15 run scoreboard players set @s rdPat 18
execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 0 if score #rdTurn rd matches 0 run scoreboard players set @s rdPat 15
# Boss test hooks (test/lock repeats, test/pattern once) only apply to the current phase.
execute if score @s rdPhase matches 0 if score #rdLock rd matches 1..7 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 2 if score #rdLock rd matches 11..18 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 0 if score #rdForce rd matches 1..7 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPhase matches 2 if score #rdForce rd matches 11..18 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPat = #rdForce rd run scoreboard players set #rdForce rd 0
scoreboard players operation @s rdPrev = @s rdPat
scoreboard players set @s rdTime 0
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
