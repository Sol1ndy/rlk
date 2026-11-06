# @s = body, at the body. #gp4Ok = 1 when nothing solid lies between her chest and the player's eyes
# (0.5 b steps; blocks outside #rlk:cm_pass block it: the arena's light layer and barrier cap pass, the
# floor and the wall ring do not; K14). No range limit: the arena is 42 b across and the pull is undodgeable.
scoreboard players set #gp4Ok mb 0
execute unless entity @e[tag=rlk_body,limit=1] run return 0
function rlk:mboss/mv/dist
scoreboard players operation #gp4Ln mb = #mbDist mb
scoreboard players set #gp4K mb 5
scoreboard players operation #gp4Ln mb /= #gp4K mb
scoreboard players set #gp4Ok mb 1
execute positioned ~ ~2.2 ~ facing entity @e[tag=rlk_body,limit=1] eyes run function rlk:mboss/guardian/p/pull/los_step
