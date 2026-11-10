# @s = a dodgeable prop in the perfect-dodge window, at it: its hit shape against the dodge's start (player/def/ghost_on).
function rlk:player/def/ghost_on
execute if score #gh cb matches 1 if score @s mbPjK matches 1 run function rlk:mboss/pj/br with storage rlk:mboss pjp
execute if score #gh cb matches 1 unless score @s mbPjK matches 1 run function rlk:mboss/pj/hr with storage rlk:mboss pjp
function rlk:player/def/ghost_off
