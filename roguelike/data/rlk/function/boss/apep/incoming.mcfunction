# Hook incoming (@s = body inside combat/apply_mods, after the level factor and mres). RES is per element (the
# registry res {"7":30,"*":10}, cm.md 8). The HP floor #mbFloor is the framework's (mboss/floor runs after this
# hook, cm.md 7.2): phase 1 = 1 % of the P1 pool (svc/floor_p1), phase 3 = 0.
