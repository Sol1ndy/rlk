# @s = body: the stretch's guaranteed P4 (see ai/pick).
scoreboard players set #gdPick mb 4
scoreboard players set #gdBag4 mb 0
scoreboard players operation #gdLast mb = #gdPick mb
function rlk:mboss/guardian/ai/launch
