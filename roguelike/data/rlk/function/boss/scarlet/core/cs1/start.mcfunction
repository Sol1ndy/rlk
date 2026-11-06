# CS1 (the next decision after the 60 % floor hit; @s = body): invulnerable until the end of CS2 / the A8 fail, cine
# (every boss hit on the player refused) 0-213, the P1 hazards cancelled, the boss bars off (FN-f; the bars hook draws
# nothing while #hud 0), the floor -> 5 %; the sequence cs1.
function rlk:boss/scarlet/core/cancel_d
kill @e[tag=rlk_hr_p]
scoreboard players set #pat hr 0
scoreboard players set #fl hr 0
scoreboard players set #ph hr 2
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
function rlk:mboss/cine/start
function rlk:mboss/bars_off
scoreboard players set #hud hr 0
scoreboard players operation #mbFloor mb = #fl5 hr
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/ground
function rlk:boss/scarlet/core/seq/cs1
