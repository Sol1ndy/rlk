# @s = body, at the body. #gp4Ok = 1 when the player is within 24 b and nothing solid lies between her
# chest and the player's eyes (0.5 b steps; blocks outside #rlk:cm_pass block it; K14).
scoreboard players set #gp4Ok mb 0
execute unless entity @e[tag=rlk_body,distance=..24,limit=1] run return 0
function rlk:mboss/mv/dist
scoreboard players operation #gp4Ln mb = #mbDist mb
scoreboard players set #gp4K mb 5
scoreboard players operation #gp4Ln mb /= #gp4K mb
scoreboard players set #gp4Ok mb 1
execute positioned ~ ~2.2 ~ facing entity @e[tag=rlk_body,limit=1] eyes run function rlk:mboss/guardian/p/pull/los_step
