execute if score @s rdPhase matches 0 store result score @s rdPat run random value 1..7
execute if score @s rdPhase matches 2 store result score @s rdPat run random value 11..18
execute if score @s rdPat = @s rdPrev run scoreboard players add @s rdPat 1
execute if score @s rdPhase matches 0 if score @s rdPat matches 8 run scoreboard players set @s rdPat 1
execute if score @s rdPhase matches 2 if score @s rdPat matches 19 run scoreboard players set @s rdPat 11
# 몽상의 일심 always follows an illusion round that was not broken (illusion/fail_end).
execute if score @s rdPhase matches 0 if score @s rdNext matches 1..7 run scoreboard players operation @s rdPat = @s rdNext
scoreboard players set @s rdNext 0
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
# A close-range pattern chosen while the player is out of its reach: close in first.
scoreboard players set @s rdGo 0
execute if score @s rdPat matches 1 at @s unless entity @e[tag=rlk_body,distance=..5.5] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 2 at @s unless entity @e[tag=rlk_body,distance=..16] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 11 at @s unless entity @e[tag=rlk_body,distance=..10] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 16 at @s unless entity @e[tag=rlk_body,distance=..11] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 17 at @s unless entity @e[tag=rlk_body,distance=..14] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 18 at @s unless entity @e[tag=rlk_body,distance=..20] run scoreboard players set @s rdGo 1
