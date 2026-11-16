# Test 30 / 35: the intro again in the fight (@s = body, invulnerable), then the fight goes on.
function rlk:boss/scarlet/core/cancel_pat0
function rlk:boss/scarlet/core/deco_seat
tp @s 884.0 201 5.0 187.31 0
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
scoreboard players set #rp hr 1
scoreboard players set #inv hr 1
scoreboard players set #sqn hr 1
scoreboard players set #sq hr 0
scoreboard players set #sqdone hr 0
scoreboard players set #skip hr 0
function rlk:boss/scarlet/seq/intro/start
