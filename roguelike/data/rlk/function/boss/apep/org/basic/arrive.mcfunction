# A melee basic on the wait ring: a socket + an attack slot if one is free, else it waits here.
scoreboard players set @s apT 0
scoreboard players set @s apS 3
function rlk:boss/apep/org/basic/try
