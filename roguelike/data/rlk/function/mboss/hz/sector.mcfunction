# Sector/arc: radius r, half-angle a degrees (1..180, 180 = full 360 swing) around the aim; option #hzR0 makes it an arc (inner part safe).
# As anything, positioned on the floor point, rotated = aim (pitch ignored). tell = ticks of telegraph
# until the hit is resolved, dmg = % of the boss base hit. Units: tenths of a block. Options: opts_reset.
# Call: function rlk:mboss/hz/sector {r:..,a:..,tell:..,dmg:..}
$scoreboard players set #hzR mb $(r)
$scoreboard players set #hzAng mb $(a)
$execute store result score #hzC mb run data get storage rlk:mboss cos[$(a)]
scoreboard players set #hzK mb 3
$scoreboard players set #hzW mb $(tell)
$scoreboard players set #hzD mb $(dmg)
function rlk:mboss/hz/make
