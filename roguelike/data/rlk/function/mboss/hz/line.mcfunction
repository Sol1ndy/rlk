# Rectangle: from the execution position forward len, total width w (option #hzBack starts it behind).
# As anything, positioned on the floor point, rotated = aim (pitch ignored). tell = ticks of telegraph
# until the hit is resolved, dmg = % of the boss base hit (0 = telegraph only). Units: tenths of a block.
# Options: opts_reset (#hzGrp = volley group, see mboss/grp_new; #hzNoDodge 1 = dash i-frames do not help;
# #hzRearm N = a hit disarms it for N ticks only, then it can hit again; live changes: hz/aim, hz/resize).
# Call: function rlk:mboss/hz/line {len:..,w:..,tell:..,dmg:..}
$scoreboard players set #hzR mb $(len)
$scoreboard players set #hzHW mb $(w)
scoreboard players set #hzK mb 4
$scoreboard players set #hzW mb $(tell)
$scoreboard players set #hzD mb $(dmg)
function rlk:mboss/hz/make
