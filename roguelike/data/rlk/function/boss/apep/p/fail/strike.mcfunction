# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# The wither: 25 % max HP, non-lethal, undodgeable (a DoT), no player-side reaction.
scoreboard players set #mbNoRx mb 1
scoreboard players set #mbDotPct mb 250
scoreboard players set #mbDotEl mb 7
scoreboard players set #mbDotLethal mb 0
function rlk:mboss/pl_dot
