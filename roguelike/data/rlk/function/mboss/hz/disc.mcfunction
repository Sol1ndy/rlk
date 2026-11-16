# Filled circle of radius r around the execution position.
# As anything, positioned on the floor point, rotated = aim (pitch ignored). tell = ticks of telegraph
# until the hit is resolved, dmg = % of the boss base hit (0 = telegraph only). Units: tenths of a block.
# Options: opts_reset (#hzGrp = volley group, see mboss/grp_new; #hzNoDodge 1 = no dodge, no i-frames;
# #hzNoParry 0 / 1 = parryable / not (default -1: hz/np_def: only no-dodge, per-mille, full-arena, mask and re-arming
# hazards; an unparriable hazard that can be dodged flashes the warning glint: hz/np_auto, or its module at the tell);
# #hzRearm N = a hit disarms it for N ticks only, then it can hit again; live changes: hz/aim, hz/resize).
# Call: function rlk:mboss/hz/disc {r:..,tell:..,dmg:..}
$scoreboard players set #hzR mb $(r)
scoreboard players set #hzK mb 1
$scoreboard players set #hzW mb $(tell)
$scoreboard players set #hzD mb $(dmg)
function rlk:mboss/hz/make
