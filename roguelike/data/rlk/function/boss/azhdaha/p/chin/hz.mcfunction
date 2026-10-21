# At the impact point, rotated along the crack line (t10): disc r 5.0 + sector r 5.6 /
# +-30 deg forward (the cracks), one volley group, 48 %, heavy KB away, ground element; quiet: no
# decal (Change note 1: the rear-up + roar is the tell); hit t35 (internal tell 25).
function rlk:mboss/grp_new
scoreboard players operation #aq1G mb = #mbGrp mb
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 4
scoreboard players set #hzKBDir mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/disc {r:50,tell:25,dmg:48}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p1h
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 4
scoreboard players set #hzKBDir mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/sector {r:56,a:30,tell:25,dmg:48}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p1h
