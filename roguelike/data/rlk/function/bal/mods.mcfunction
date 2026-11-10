# @s = enemy with a gauge, in combat/apply_mods (after element/on_hit, before the boss incoming hooks / HP floors; never
# true damage): a groggy enemy takes the tier %, else a burst hit / a strong reaction takes balance (not on a killing blow)
execute if score @s grgT matches 1.. run return run function rlk:bal/amp
execute unless score #burstDmg tmp matches 1.. unless score #rx tmp matches 1.. run return 0
execute if score #dmg tmp >= @s mhpC run return 0
function rlk:bal/src/hit
