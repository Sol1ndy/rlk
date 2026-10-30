# g.cast_end(): the cast slot part is over; 32's cooldown starts here (31's at the orbs' end, bg/end_l).
execute if score #azCast mb matches 32 run scoreboard players operation #azCdE32 mb = #azClk mb
execute if score #azCast mb matches 32 run scoreboard players add #azCdE32 mb 600
scoreboard players set #azCast mb 0
