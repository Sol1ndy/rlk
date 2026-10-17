# From combat/apply right after element/on_hit (@s = aux with rlk_mb_hit; #dmg #elem #elU #rx #tfm #crit
# known). RES (mres) applies first, then the module hook may change #dmg or take over completely
# (#mbAuxDone mb 1); by default #dmg comes off the aux's mhpC with a number. Nothing here re-enters
# combat/apply; a broken aux gets rlk_mb_broken and the module acts on it in its tick.
execute if entity @s[tag=rlk_mb_broken] run return 0
scoreboard players set #hitLanded tmp 1
scoreboard players set #mbAuxDone mb 0
execute unless score @s mres matches 0 if score #dmg tmp matches 1.. run function rlk:combat/res
function rlk:mboss/d/aux_hit
execute if score #mbAuxDone mb matches 1 run return 0
function rlk:mboss/aux/take
