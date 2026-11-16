# From room/mob_wave (@s = the rift's zone marker, at it; #spOn 1, #combat = its zid): the special named by the zone.
execute unless data entity @s data.rift.id run return run function rlk:mboss/start_cancel
function rlk:mboss/sp/start with entity @s data.rift
