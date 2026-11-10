# @s = a dodgeable hazard that missed the body in the perfect-dodge window: the same test with the body mark on the dodge's
# start (player/def/ghost_on: the rlk_dgo box; nothing when it is gone).
function rlk:player/def/ghost_on
execute if score #gh cb matches 1 run function rlk:mboss/hz/hit1
function rlk:player/def/ghost_off
