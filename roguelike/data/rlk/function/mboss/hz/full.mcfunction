# The whole arena; option #hzR0 = safe circle (radius, tenths) around the execution position.
# As anything, positioned on the floor point, rotated = aim (pitch ignored). tell = ticks of telegraph
# until the hit is resolved, dmg = % of the boss base hit. Units: tenths of a block. Options: opts_reset.
# Call: function rlk:mboss/hz/full {tell:..,dmg:..}
scoreboard players set #hzR mb 210
scoreboard players set #hzK mb 5
$scoreboard players set #hzW mb $(tell)
$scoreboard players set #hzD mb $(dmg)
function rlk:mboss/hz/make
