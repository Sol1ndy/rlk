# The intro is over (its end, the framework cap, a reload or a test; @s = body): the fight state, P1 with the 60 % floor,
# the title / music 1 (the end state of the full intro), the skip prompt gone.
function rlk:mboss/intro_end
execute unless score #ph hr matches 0 run return 0
function rlk:boss/scarlet/core/skip_clear
scoreboard players set #ph hr 1
scoreboard players set #sqn hr 0
scoreboard players set #sq hr 0
scoreboard players set #sqdone hr 0
scoreboard players set #pat hr 0
scoreboard players set #inv hr 0
scoreboard players set #rp hr 0
function rlk:mboss/title {title:"홍련",sub:"월하곡",color:"#E8466A"}
execute unless score #mbMusPh mb matches 1 run function rlk:mboss/music/set {ph:1}
function rlk:boss/scarlet/core/floors
scoreboard players operation #mbFloor mb = #fl60 hr
kill @e[tag=rlk_hr_deco_seat_rock]
function rlk:boss/scarlet/ai/phase
function rlk:boss/scarlet/core/looks
function rlk:boss/scarlet/ai/rec_start
scoreboard players set #rec hr 20
