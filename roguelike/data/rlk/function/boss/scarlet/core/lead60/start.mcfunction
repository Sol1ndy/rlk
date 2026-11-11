# lead60 tick 0 (CS1 ended, a reload / pause in CS1 or lead60, tests; @s = body): cine off, the bars back with the gauge
# 5/5 under them (the refill of its tick 0), no balance damage until P2 (#mbBalOff), the G1 chain (#gk 1; its fail is
# lethal only with ULT60_LETHAL: #warn).
function rlk:mboss/cine/end
function rlk:mboss/bars_on
scoreboard players set #hud hr 1
function rlk:boss/scarlet/shield/arm
scoreboard players set #ph hr 3
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
scoreboard players set #mbBalOff mb 1
function rlk:boss/scarlet/core/skip_clear
scoreboard players set #gk hr 1
scoreboard players set #warn hr 0
function rlk:boss/scarlet/core/looks
function rlk:boss/scarlet/core/seq/lead60
