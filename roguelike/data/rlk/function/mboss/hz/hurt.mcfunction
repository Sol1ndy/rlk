# One hit per hazard: a dodge (dash i-frames) also consumes it. #hzRearm hazards arm again mbHzRA ticks later;
# #hzNoDodge hazards ignore the dash i-frames (mboss/hurt with #mbNoDodge 1).
scoreboard players set @s mbHzHit 1
execute if score @s mbHzRA matches 1.. run function rlk:mboss/hz/rearm_at
scoreboard players set #hzHit mb 1
scoreboard players operation #mbHitPct mb = @s mbHzD
scoreboard players operation #cmEl tmp = @s mbHzE
scoreboard players operation #mbKB mb = @s mbHzB
scoreboard players operation #mbKBDir mb = @s mbHzKD
scoreboard players operation #mbNoDodge mb = @s mbHzND
scoreboard players operation #mbNoRx mb = @s mbHzNR
scoreboard players set #mbSrc mb 1
function rlk:mboss/hurt
scoreboard players set #mbNoDodge mb 0
scoreboard players operation #g mb = @s mbHzG
execute if score #dodged tmp matches 0 if score #g mb matches 1.. run function rlk:mboss/grp_mark
