scoreboard players set @s mbPjHit 1
scoreboard players operation #mbHitPct mb = @s mbPjD
scoreboard players operation #cmEl tmp = @s mbPjE
scoreboard players operation #mbKB mb = @s mbPjB
scoreboard players set #mbKBDir mb 1
function rlk:mboss/hurt
scoreboard players set #pjEv mb 4
scoreboard players set #pjKeep mb 1
function rlk:mboss/d/pj_end
