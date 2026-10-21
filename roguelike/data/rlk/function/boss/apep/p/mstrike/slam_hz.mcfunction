# At S (t46): the belly-flop slam r 4.2 (tell 15, hit t61), quiet (none row: the
# hoop 44-49 and the roll 49-61 are the tell); a new volley group shared with the tail whip.
function rlk:mboss/grp_new
scoreboard players operation #apq31G mb = #mbGrp mb
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
function rlk:mboss/hz/disc {r:42,tell:15,dmg:150}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p31h
