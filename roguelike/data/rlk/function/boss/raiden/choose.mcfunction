execute if score @s rdPhase matches 0 run function rlk:boss/raiden/bag/draw_0
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/bag/draw_2
# 몽상의 일심 always follows an illusion round that was not broken (illusion/fail_end).
execute if score @s rdPhase matches 0 if score @s rdNext matches 1..7 run scoreboard players operation @s rdPat = @s rdNext
scoreboard players set @s rdNext 0
scoreboard players add @s rdTurns 1
scoreboard players operation #rdTurn rd = @s rdTurns
scoreboard players operation #rdTurn rd %= #rd4 rd
# Tenma picks (plan A.4), later lines win: 18 when the player is >= 10 b away and the last pick was not 18; 20 when
# the player stood in her rear cone at the end of the last pattern (tm/after) and its 300 t cooldown is over; the 40 %
# chain after 16 (17 or 11); 15 replaces the fourth pick once per transformation.
execute if score @s rdPhase matches 2 unless score @s rdPrev matches 18 at @s unless entity @e[tag=rlk_body,distance=..10] run scoreboard players set @s rdPat 18
execute if score @s rdPhase matches 2 if entity @s[tag=rlk_rd_tm_rear] if score @s rdTmCD matches ..0 run scoreboard players set @s rdPat 20
execute if score @s rdPhase matches 2 if score @s rdTmChain matches 1.. run scoreboard players operation @s rdPat = @s rdTmChain
execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 0 if score #rdTurn rd matches 0 run scoreboard players set @s rdPat 15
scoreboard players set @s rdTmChain 0
tag @s remove rlk_rd_tm_rear
# Boss test hooks (test/lock repeats, test/pattern once) only apply to the current phase.
execute if score @s rdPhase matches 0 if score #rdLock rd matches 1..7 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 2 if score #rdLock rd matches 11..20 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 0 if score #rdForce rd matches 1..7 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPhase matches 2 if score #rdForce rd matches 11..20 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPat = #rdForce rd run scoreboard players set #rdForce rd 0
# Whatever finally runs (bag, forced follow-up, ultimate, test hook) leaves the bag.
execute if score @s rdPat matches 1 run scoreboard players set #rdB1 rd 0
execute if score @s rdPat matches 2 run scoreboard players set #rdB2 rd 0
execute if score @s rdPat matches 3 run scoreboard players set #rdB3 rd 0
execute if score @s rdPat matches 4 run scoreboard players set #rdB4 rd 0
execute if score @s rdPat matches 5 run scoreboard players set #rdB5 rd 0
execute if score @s rdPat matches 6 run scoreboard players set #rdB6 rd 0
execute if score @s rdPat matches 7 run scoreboard players set #rdB7 rd 0
execute if score @s rdPat matches 11 run scoreboard players set #rdB11 rd 0
execute if score @s rdPat matches 12 run scoreboard players set #rdB12 rd 0
execute if score @s rdPat matches 13 run scoreboard players set #rdB13 rd 0
execute if score @s rdPat matches 14 run scoreboard players set #rdB14 rd 0
execute if score @s rdPat matches 16 run scoreboard players set #rdB16 rd 0
execute if score @s rdPat matches 17 run scoreboard players set #rdB17 rd 0
execute if score @s rdPat matches 19 run scoreboard players set #rdB19 rd 0
scoreboard players operation @s rdPrev = @s rdPat
scoreboard players set @s rdTime 0
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
# A close-range pattern chosen while the player is out of its reach: close in first.
scoreboard players set @s rdGo 0
execute if score @s rdPat matches 1 at @s unless entity @e[tag=rlk_body,distance=..5.5] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 2 at @s unless entity @e[tag=rlk_body,distance=..16] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 11 at @s unless entity @e[tag=rlk_body,distance=..8] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 16 at @s unless entity @e[tag=rlk_body,distance=..9] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 19 at @s unless entity @e[tag=rlk_body,distance=..14] run scoreboard players set @s rdGo 1
