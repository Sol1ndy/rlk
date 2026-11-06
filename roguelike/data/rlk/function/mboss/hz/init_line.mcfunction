# len = mbHzR, back = mbHzR0; half width (tenths of the full width x 50) with the body pad.
scoreboard players operation @s mbHzHW = #hzHW mb
scoreboard players operation @s mbHzHW *= #c100 mb
scoreboard players operation @s mbHzHW /= #c2 mb
scoreboard players operation @s mbHzC = @s mbHzHW
scoreboard players add @s mbHzHW 300
scoreboard players operation @s mbHzR0 = #hzBack mb
scoreboard players operation @s mbHzR0 *= #c100 mb
scoreboard players operation @s mbHzLo = @s mbHzR0
scoreboard players operation @s mbHzLo *= #cm1 mb
scoreboard players remove @s mbHzLo 300
scoreboard players operation @s mbHzHi = @s mbHzR
scoreboard players add @s mbHzHi 300
