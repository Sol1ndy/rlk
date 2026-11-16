# Rig objectives (safe on every load). knRigC clip id, knRigT clip tick (-1 = queued), knRigF hit flash, knRigY face scratch,
# knRigS state (0 normal, 1 hidden), knRigForm (0 p1, 1 p2), stored looks knRigWi wings, knRigWr / knRigWl weapons, knRigGl glow,
# knRigPr props (indices of api.LOOKS); knRigFl the follow list, knRigQ* the follow cache. The anchor table (storage rlk:kn rig.an)
# is loaded once per version.
scoreboard objectives add knRigC dummy
scoreboard objectives add knRigT dummy
scoreboard objectives add knRigF dummy
scoreboard objectives add knRigY dummy
scoreboard objectives add knRigS dummy
scoreboard objectives add knRigForm dummy
scoreboard objectives add knRigWi dummy
scoreboard objectives add knRigWr dummy
scoreboard objectives add knRigWl dummy
scoreboard objectives add knRigGl dummy
scoreboard objectives add knRigPr dummy
scoreboard objectives add knRigFl dummy
scoreboard objectives add knRigQ dummy
scoreboard objectives add knRigQx dummy
scoreboard objectives add knRigQy dummy
scoreboard objectives add knRigQz dummy
scoreboard objectives add knRigQw dummy
execute unless data storage rlk:kn rig{anv:190586752} run function rlk:boss/arlecchino/rig/an/load
