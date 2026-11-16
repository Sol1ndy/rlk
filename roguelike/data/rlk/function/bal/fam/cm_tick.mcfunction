# @s = groggy cm brain (cm/tick, after the freeze line): not free, held in place, stunned for the group starts
# (pack_go / line_go / pair_go skip stunned members, rv/fly hangs), nothing started
scoreboard players set #free tmp 0
scoreboard players set #hold tmp 1
execute unless score @s stunT matches 2.. run scoreboard players set @s stunT 2
function rlk:bal/fam/cm_hold
execute if score @s cmS matches 1.. run function rlk:cm/cancel
