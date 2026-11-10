# @s = a hazard marker, at / rotated as it (mboss/near_all, only while the perfect-dodge window is open). A dodgeable hazard in its
# active window that has not hit (this tick's hz/tick test missed the moved body) runs the same test with the body mark on
# the dodge's start (player/def/ghost_on: the rlk_dgo box; nothing when it is gone). Not for a no-dodge hazard.
execute unless score @s mbHzHit matches 0 run return 0
execute unless score @s mbHzD matches 1.. run return 0
execute unless score @s mbHzND matches 0 run return 0
execute if score @s mbHzT < @s mbHzW run return 0
scoreboard players operation #hzEnd mb = @s mbHzW
scoreboard players operation #hzEnd mb += @s mbHzA
execute if score @s mbHzT >= #hzEnd mb run return 0
function rlk:player/def/ghost_on
execute if score #gh cb matches 1 run function rlk:mboss/hz/hit
function rlk:player/def/ghost_off
