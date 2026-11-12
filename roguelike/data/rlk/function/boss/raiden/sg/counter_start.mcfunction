# sg/guard_parry (a player hit, outside the boss tick): queue the counter; its c0 runs on the next boss tick
# (sg/counter_tick: c = rdSgCt - 2), so every counter hit counts from the boss clock. rdSgCk = the weapon.
scoreboard players set @s rdSgCt 1
scoreboard players set @s rdSgCcd 60
scoreboard players operation @s rdSgCk = @s rdWpn
