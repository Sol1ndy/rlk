# One hit per prop. Event 4 with #pjKeep 1 preset (the prop pierces and flies on, harmless from now);
# the hook sets #pjKeep mb 0 to end the flight here (pj/tick removes the prop after this sub-step).
scoreboard players set @s mbPjHit 1
scoreboard players operation #mbHitPct mb = @s mbPjD
scoreboard players operation #cmEl tmp = @s mbPjE
scoreboard players operation #mbKB mb = @s mbPjB
scoreboard players set #mbKBDir mb 1
scoreboard players operation #mbNoDodge mb = @s mbPjND
scoreboard players operation #mbNoRx mb = @s mbPjNR
scoreboard players set #mbSrc mb 2
function rlk:mboss/hurt
scoreboard players set #mbNoDodge mb 0
scoreboard players operation #g mb = @s mbPjG
execute if score #dodged tmp matches 0 if score #g mb matches 1.. run function rlk:mboss/grp_mark
scoreboard players set #pjEv mb 4
scoreboard players set #pjKeep mb 1
function rlk:mboss/d/pj_end
execute if score #pjKeep mb matches 0 run scoreboard players set #pjStop mb 2
