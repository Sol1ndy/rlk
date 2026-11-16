# @s = a new unparriable hazard (mbHzNP 1, or 2 = the module warns for it itself: mboss_lib.hz_opts(noparry=1, glint=False);
# stored as 1). The warning glint means "this cannot be parried: dodge it" (reviews B-02 / B-04), so the framework flashes
# it here only for a hazard that hits, can be dodged (not #hzNoDodge: those are answered by position and keep their own
# tells), is a strike (not #hzRearm: a lingering field / beam) and whose own wind-up is the tell: made at least
# 12 t before its strike. A hazard made later than that (a strike-frame hazard) is announced by its module at the
# pattern's tell tick (mboss/np_glint or np_glint_here from there), never 1 t before the hit.
execute if score @s mbHzNP matches 2 run return run scoreboard players set @s mbHzNP 1
execute unless score @s mbHzD matches 1.. run return 0
execute if score @s mbHzND matches 1 run return 0
execute if score @s mbHzRA matches 1.. run return 0
execute if score @s mbHzW matches ..11 run return 0
function rlk:mboss/np_glint
