scoreboard players operation #bOff tmp = @s bowQo
scoreboard players set #bFin tmp 0
scoreboard players set @s bowQ -1
scoreboard players operation #bCoef tmp = @s bowQc
function rlk:char/bow/na_shot
execute unless score #k234 snd matches 1 run function rlk:snd/f261
