# @s = a prop, at / rotated as it (mboss/near_all, only while the perfect-dodge window is open, after every prop moved this tick):
# a dodgeable prop that has not hit is tested at its position against the dodge's start (player/def/ghost_on; a contact
# there is judged as a perfect dodge; its pj_end hook runs as on any hit).
execute unless score @s mbPjHit matches 0 run return 0
execute unless score @s mbPjD matches 1.. run return 0
execute unless score @s mbPjND matches 0 run return 0
execute store result storage rlk:mboss pjp.hr int 1 run scoreboard players get @s mbPjR
scoreboard players set #pjStop mb 0
function rlk:player/def/ghost_on
execute if score #gh cb matches 1 if score @s mbPjK matches 1 run function rlk:mboss/pj/br with storage rlk:mboss pjp
execute if score #gh cb matches 1 unless score @s mbPjK matches 1 run function rlk:mboss/pj/hr with storage rlk:mboss pjp
function rlk:player/def/ghost_off
execute if score #pjStop mb matches 2 run kill @s
