# One player DoT tick (cm.md 13.4), as anything: #mbDotPct mb = per mille of the player's max HP, #mbDotEl mb = #elem for
# the shields (an element shield of the same element absorbs at 250 %), #mbDotLethal mb 0 = the player keeps >= 1 HP.
# Guard shield, then the element shield; no defence; dash i-frames do not block it; hurt fx. Output #mbDotDmg (HP lost).
# Refused (nothing, #mbDotDmg 0) while dead, reviving, on a selection screen, the boss dying (#mbSt 2) or #mbCine 1.
scoreboard players set #mbDotDmg mb 0
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run function rlk:mboss/pl_dot_end
execute if entity @a[tag=player,scores={rnDie=1..}] run return run function rlk:mboss/pl_dot_end
execute if entity @a[tag=player,scores={pkMode=1..}] run return run function rlk:mboss/pl_dot_end
execute if score #mbSt mb matches 2 run return run function rlk:mboss/pl_dot_end
execute if score #mbCine mb matches 1 run return run function rlk:mboss/pl_dot_end
execute as @a[tag=player,limit=1] at @s run function rlk:mboss/pl_dot2
function rlk:mboss/pl_dot_end
