# Hook reload (@s = body after /reload; every aux entity is gone: rig parts, stars, fx, props).
# AI back to idle with HP kept; a guard pair restarts soon, an interrupted chaos is abandoned.
function rlk:mboss/guardian/ai/consts
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
# a glide or flight the reloaded AI no longer owns (P5 under the ring, chaos travel) stops here
execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
function rlk:mboss/guardian/p/cancel
execute if score #gdSt mb matches 3 run scoreboard players set #gdLeft mb 0
execute if score #gdSt mb matches 4..6 run function rlk:mboss/guardian/chaos/reset
execute if score #gdSt mb matches 4..6 run scoreboard players set #gdLeft mb 4
scoreboard players set #gdRecOn mb 0
scoreboard players set #gdRecNew mb 0
scoreboard players set #gdBq1 mb 0
scoreboard players set #gdBq2 mb 0
scoreboard players set #gdStars mb 0
scoreboard players set #gdHaze mb 0
scoreboard players set #gdTim mb 0
scoreboard players set #mbNoLeash mb 0
tag @s remove rlk_mb_inv
function rlk:mboss/guardian/rig/glow/off
function rlk:mboss/guardian/rig/spawn
function rlk:mboss/guardian/rig/spear/geo
function rlk:mboss/guardian/look/eye_rest
scoreboard players set #gdCool mb 20
function rlk:mboss/guardian/ai/enter
