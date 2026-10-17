# One hit per prop. Event 4 with #pjKeep 1 preset (the prop pierces and flies on, harmless from now);
# the hook sets #pjKeep mb 0 to end the flight here (pj/tick removes the prop after this sub-step).
scoreboard players set @s mbPjHit 1
scoreboard players operation #mbHitPct mb = @s mbPjD
scoreboard players operation #cmEl tmp = @s mbPjE
scoreboard players operation #mbKB mb = @s mbPjB
scoreboard players set #mbKBDir mb 1
function rlk:mboss/hurt
scoreboard players set #pjEv mb 4
scoreboard players set #pjKeep mb 1
function rlk:mboss/d/pj_end
execute if score #pjKeep mb matches 0 run scoreboard players set #pjStop mb 2
