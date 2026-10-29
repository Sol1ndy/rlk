# @s = the open rift's anchor, at it: enter it as a click would (room/rift/enter); refused (arena busy): try again in 5 t.
function rlk:room/rift/enter
execute if score #spOn mb matches 1 run return run scoreboard players set #spAuto mb 0
schedule function rlk:mboss/test/swait 5t replace
