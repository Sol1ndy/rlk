# Annulus r0..r (the hole is safe). For a jumpable wave set #hzY1 small (e.g. 7 = 0.7 b).
# As anything, positioned on the floor point, rotated = aim (pitch ignored). tell = ticks of telegraph
# until the hit is resolved, dmg = % of the boss base hit (0 = telegraph only). Units: tenths of a block.
# Options: opts_reset (#hzGrp = volley group, see mboss/grp_new; #hzNoDodge 1 = dash i-frames do not help;
# #hzRearm N = a hit disarms it for N ticks only, then it can hit again; live changes: hz/aim, hz/resize).
# Call: function rlk:mboss/hz/ring {r0:..,r:..,tell:..,dmg:..}
$scoreboard players set #hzR mb $(r)
$scoreboard players set #hzR0 mb $(r0)
scoreboard players set #hzK mb 2
$scoreboard players set #hzW mb $(tell)
$scoreboard players set #hzD mb $(dmg)
function rlk:mboss/hz/make
