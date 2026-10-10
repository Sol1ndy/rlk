# Orphan cleanup for interruption, reload or failed flower: no stale gauge.
execute unless entity @e[tag=rlk_rd_object,scores={rdObjKind=3}] run kill @e[tag=rlk_rd_orb]
