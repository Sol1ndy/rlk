# Test 30: straight to P2 (HP at most the floor above it).
execute unless function rlk:boss/tachy/core/force run return 0
scoreboard players set #fl tk 1
scoreboard players set #flnext tk 0
scoreboard players set #ph tk 4
function rlk:boss/tachy/mantle/cancel
execute if score @s mhpC > #fl70 tk run scoreboard players operation @s mhpC = #fl70 tk
scoreboard players operation #mbFloor mb = #fl35 tk
function rlk:boss/tachy/ai/phase
function rlk:boss/tachy/core/looks
scoreboard players set #pat tk 0
function rlk:boss/tachy/ai/rec_start
function rlk:boss/tachy/hud/sub
