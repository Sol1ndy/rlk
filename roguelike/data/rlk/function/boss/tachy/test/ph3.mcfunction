# Test 31: straight to P3 (HP at most the floor above it).
execute unless function rlk:boss/tachy/core/force run return 0
scoreboard players set #fl tk 2
scoreboard players set #flnext tk 0
scoreboard players set #ph tk 7
function rlk:boss/tachy/mantle/cancel
execute if score @s mhpC > #fl35 tk run scoreboard players operation @s mhpC = #fl35 tk
scoreboard players set #mbFloor mb 0
function rlk:mboss/music/set {ph:2}
function rlk:boss/tachy/ai/phase
function rlk:boss/tachy/core/looks
scoreboard players set #pat tk 0
function rlk:boss/tachy/ai/rec_start
function rlk:boss/tachy/hud/sub
