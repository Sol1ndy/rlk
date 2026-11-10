# @s = hazard marker, at @s, inside its active window. Body feet only (never the camera): hz/hit1. Combat overhaul C: while
# the perfect-dodge window is open (#dgOpen cb 1: the dodge started this tick or the 2 before, so the body has already moved
# 1-3 b), a hazard that missed the body is tested once more at the dodge's start (hz/hit_near): a contact there is judged
# as a perfect dodge (never damage). Not for a no-dodge hazard (it would have hit the body that stayed).
function rlk:mboss/hz/hit1
execute if score #hzHit mb matches 0 if score #dgOpen cb matches 1 if score @s mbHzND matches 0 run function rlk:mboss/hz/hit_near
