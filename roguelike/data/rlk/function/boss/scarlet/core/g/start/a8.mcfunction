# A8 자영 연참 from T0 (@s = body; SQ1 / a lead-in ended, tests): the gauntlet clock #pt, its judge
# result cleared; invulnerable (the ghost body; only the scripted true damage passes).
function rlk:boss/scarlet/core/stop_move
scoreboard players set #ph hr 4
scoreboard players set #gk hr 1
scoreboard players set #pat hr 21
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #gres hr 0
scoreboard players set #sqn hr 0
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
scoreboard players set #warn hr 0
function rlk:boss/scarlet/p/a8/start
