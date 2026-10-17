# One hit per hazard: a dodge (dash i-frames) also consumes it.
scoreboard players set @s mbHzHit 1
scoreboard players set #hzHit mb 1
scoreboard players operation #mbHitPct mb = @s mbHzD
scoreboard players operation #cmEl tmp = @s mbHzE
scoreboard players operation #mbKB mb = @s mbHzB
scoreboard players operation #mbKBDir mb = @s mbHzKD
function rlk:mboss/hurt
