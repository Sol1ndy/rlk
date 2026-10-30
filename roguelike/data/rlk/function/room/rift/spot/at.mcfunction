# {x,y,z} (@s = the zone marker): the block centre of the candidate, the ground found upward (<= 5 b, as room/mob_up).
scoreboard players set #riftU room 0
$execute positioned $(x) $(y) $(z) positioned ~0.5 ~ ~0.5 run function rlk:room/rift/spot/up
