# Hook tick (@s = body, at @s, fight state). Order: clocks, stars and their queued punishments (true
# damage, can be lethal), AI state, pattern slot, then the rig (a clip played this tick starts this tick).
scoreboard players add #gdClk mb 1
execute if score #gdVoCd mb matches 1.. run scoreboard players remove #gdVoCd mb 1
execute if score #gdVoG mb matches 1.. run scoreboard players remove #gdVoG mb 1
execute if score #gdFlash mb matches 1 unless score @s gdRigF matches 1.. run function rlk:mboss/guardian/rig/flash
scoreboard players set #gdFlash mb 0
execute if score #gdStars mb matches 1.. run function rlk:mboss/guardian/star/tick
execute if score #gdBq1 mb matches 1.. run function rlk:mboss/guardian/star/bq1
execute unless score #mbSt mb matches 1 run return 0
execute if score #gdBq2 mb matches 1.. run function rlk:mboss/guardian/star/bq2
execute unless score #mbSt mb matches 1 run return 0
function rlk:mboss/guardian/ai/state
execute if score #gdPat mb matches 1.. run function rlk:mboss/guardian/p/run
function rlk:mboss/guardian/rig/tick
