# cm brain: the freeze path without the ice — the running attack is cancelled (lines, fireballs, cannon aim, charge
# tag; elites reset on their next tick: dash targets, nj visible, cs surfaced), the drummer stops, AI off, held
scoreboard players operation #cid tmp = @s cmId
function rlk:cm/cancel
execute if entity @s[tag=rlk_cm_dr] run function rlk:cm/dr/interrupt
function rlk:bal/fam/noai_on
scoreboard players set @s stunT 2
function rlk:bal/fam/cm_hold
