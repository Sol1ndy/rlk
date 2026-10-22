# @s = the body (the anchor), at it, rotated as it: mboss/world after body_tick while #mbPushOn 1 (a per-tick request of
# the module; cm.md 13.5). Capsules = rlk:mboss push[] {f0,f1,hw,px,top} in tenths in the anchor frame (f0 <= f <= f1,
# |s| < hw; an entry with px is active only while that proxy's current top <= top). A player inside is moved toward the
# nearest exit (side, front end, back end) whose end point is not inside a live disc / ring / line hazard, by at most
# 0.6 b this tick in 0.1-b player/knockback/check steps (no velocity, no FOV). Refused while dead, reviving, selecting,
# in the map view or dashing.
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if entity @a[tag=player,scores={vMap=1}] run return 0
execute if entity @a[tag=player,scores={dashMoveT=1..}] run return 0
execute unless data storage rlk:mboss push[0] run return 0
execute unless function rlk:mboss/mv/local run return 0
scoreboard players operation #pbx mb = #mbPX mb
scoreboard players operation #pbz mb = #mbPZ mb
scoreboard players set #puDone mb 0
data modify storage rlk:mboss pq set from storage rlk:mboss push
function rlk:mboss/push/cap_loop
execute if score #puDone mb matches 1 run scoreboard players set #mbPlG mb -1
