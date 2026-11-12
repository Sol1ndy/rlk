# The intro is over (its end, the framework cap, a reload or a test; @s = body): the fight state, P1a, the 70 % floor.
function rlk:mboss/intro_end
execute unless score #ph kn matches 0 run return 0
scoreboard players set #ph kn 1
scoreboard players set #sq kn 0
scoreboard players set #sqdone kn 0
scoreboard players set #pat kn 0
function rlk:boss/arlecchino/core/floors
scoreboard players operation #mbFloor mb = #fl70 kn
function rlk:boss/arlecchino/ai/phase
function rlk:boss/arlecchino/core/looks
function rlk:boss/arlecchino/ai/sample
function rlk:boss/arlecchino/ai/rec_start
scoreboard players set #rec kn 20
function rlk:boss/arlecchino/hud/sub
