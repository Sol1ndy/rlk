# GENERATED from the registry (kind chapter: ch + route). From room/pick/boss: the boss map's layout. A test forces a
# chapter boss through #cbForce (honoured only while #mbTest 1); every other chapter not routed here is Raiden's.
execute if score #mbTest mb matches 1 if score #cbForce mb matches 1.. run return run function rlk:mboss/cb/route_force
function rlk:room/raiden/layout
