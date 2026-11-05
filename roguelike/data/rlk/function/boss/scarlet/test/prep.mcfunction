# The chain context from P2 on (tests; @s = body): the 5 % floor, the bars and the module HUD on, phase p2 looks,
# music 2, the crimson look.
scoreboard players operation #mbFloor mb = #fl5 hr
function rlk:mboss/bars_on
scoreboard players set #hud hr 1
scoreboard players set #fl hr 0
scoreboard players set #ph hr 7
function rlk:boss/scarlet/core/looks
execute unless score #mbMusPh mb matches 2 run function rlk:mboss/music/set {ph:2}
