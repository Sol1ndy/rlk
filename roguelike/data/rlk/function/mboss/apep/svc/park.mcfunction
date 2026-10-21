# R10 (plan 7.2): the body parked 30 b above the centre (NoGravity husk, rlk_mb_inv through the px set
# parked, husk 0.1, no shield), the rig parked, #mbNoLeash 1 (re-set by every reload: rl/p2). Keeps rlk_zmob
# (the zone cannot clear) and stays the bars carrier.
scoreboard players set #apPark mb 1
scoreboard players set #mbNoLeash mb 1
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s 440 231 8 0 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/apep/rig_stub/park
function rlk:mboss/apep/px/parked
