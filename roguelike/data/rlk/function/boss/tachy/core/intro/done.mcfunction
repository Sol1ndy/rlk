# The intro is over (its end, the framework cap, a reload or a test; @s = body): the fight state, P1, the floors.
function rlk:mboss/intro_end
execute unless score #ph tk matches 0 run return 0
scoreboard players set #ph tk 1
scoreboard players set #sq tk 0
scoreboard players set #sqdone tk 0
scoreboard players set #pat tk 0
function rlk:boss/tachy/core/floors
execute if score #fl tk matches 0 run scoreboard players operation #mbFloor mb = #fl70 tk
function rlk:boss/tachy/ai/phase
function rlk:boss/tachy/core/looks
function rlk:boss/tachy/ai/sample
function rlk:boss/tachy/ai/rec_start
scoreboard players set #rec tk 20
function rlk:boss/tachy/el/badge
function rlk:boss/tachy/hud/sub
