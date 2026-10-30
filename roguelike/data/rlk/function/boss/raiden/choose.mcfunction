# As the boss at its feet (idle, rdCool 0). Phase 0: forced picks, reactive rear checks, then the weapon bag with
# the range fit (shogun.py sg/choose). Phase 2: the Tenma bag and tenma.CHOOSE_RULES.
scoreboard players set @s rdPat 0
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/choose
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/bag/draw_2
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
execute if score @s rdPhase matches 0 if score #rdLock rd matches 1..10 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 0 if score #rdLock rd matches 21..28 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 2 if score #rdLock rd matches 11..20 run scoreboard players operation @s rdPat = #rdLock rd
execute if score @s rdPhase matches 0 if score #rdForce rd matches 1..10 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPhase matches 0 if score #rdForce rd matches 21..28 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPhase matches 2 if score #rdForce rd matches 11..20 run scoreboard players operation @s rdPat = #rdForce rd
execute if score @s rdPat = #rdForce rd run scoreboard players set #rdForce rd 0
# Whatever finally runs (bag, forced follow-up, ultimate, test hook) leaves the bag.
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/picked
execute if score @s rdPhase matches 2 if score @s rdPat matches 11 run scoreboard players set #rdB11 rd 0
execute if score @s rdPhase matches 2 if score @s rdPat matches 12 run scoreboard players set #rdB12 rd 0
execute if score @s rdPhase matches 2 if score @s rdPat matches 13 run scoreboard players set #rdB13 rd 0
execute if score @s rdPhase matches 2 if score @s rdPat matches 14 run scoreboard players set #rdB14 rd 0
execute if score @s rdPhase matches 2 if score @s rdPat matches 16 run scoreboard players set #rdB16 rd 0
execute if score @s rdPhase matches 2 if score @s rdPat matches 17 run scoreboard players set #rdB17 rd 0
execute if score @s rdPhase matches 2 if score @s rdPat matches 19 run scoreboard players set #rdB19 rd 0
scoreboard players operation @s rdPrev = @s rdPat
scoreboard players set @s rdTime 0
# Face the player; the rear checks (25, 26) strike straight behind her, so they keep her facing.
execute unless score @s rdPat matches 25..26 at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute unless score @s rdPat matches 25..26 at @s rotated as @s run tp @s ~ ~ ~ ~ 0
# A pattern chosen while the player is out of its reach (REACH start) or too near (REACH_MIN) blinks first.
scoreboard players set @s rdGo 0
execute if score @s rdPat matches 11 at @s unless entity @e[tag=rlk_body,distance=..8] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 16 at @s unless entity @e[tag=rlk_body,distance=..9] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 19 at @s unless entity @e[tag=rlk_body,distance=..14] run scoreboard players set @s rdGo 1
execute if score @s rdPat matches 19 at @s if entity @e[tag=rlk_body,distance=..6] run scoreboard players set @s rdGo 1
