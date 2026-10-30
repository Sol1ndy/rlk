# The special was killed (@s = the rift's zone marker): the zone's rift is done (rlk_riftz -> rlk_riftdone: no rift
# hook fires on it again), the reward, the test replay links, forget. Returns 1.
tag @s remove rlk_riftz
tag @s add rlk_riftdone
function rlk:mboss/sp/reward
execute if score #mbTest mb matches 1 if data storage rlk:mboss cur run function rlk:mboss/test/won with storage rlk:mboss cur
function rlk:mboss/forget
return 1
