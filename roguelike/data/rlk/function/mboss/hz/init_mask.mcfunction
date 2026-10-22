# @s = a new mask hazard: the safe distance squared with the 0.3 b pad, milliblocks.
scoreboard players operation #t mb = @s mbHzR0
scoreboard players add #t mb 300
scoreboard players operation @s mbHzRI = #t mb
scoreboard players operation @s mbHzRI *= #t mb
