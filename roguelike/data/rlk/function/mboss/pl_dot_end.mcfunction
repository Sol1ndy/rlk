# Every pl_dot input is reset after the call, refused or not (a stale value never leaks into the next caller). A one-shot
# #mbNoRx the caller set for this tick is spent here too (pl_dot never runs a player reaction), so it cannot reach the
# next direct mboss/hurt.
scoreboard players set #mbDotPct mb 0
scoreboard players set #mbDotEl mb 0
scoreboard players set #mbDotLethal mb 0
scoreboard players set #mbNoRx mb 0
