# Rig objectives (safe on every load). hrRigC clip id, hrRigT clip tick (-1 = queued), hrRigF hit flash, hrRigY face scratch,
# hrRigS state (0 normal, 1 hidden), stored looks hrRigForm / Ph / Bl / Fc / HR / HL / Hat / Sw / Sc / Pr / Cu / Bo (indices of
# api.LOOKS, HANDS, PROP_STATES); hrRigQ* the follow cache. The anchor table (storage rlk:hr rig.an) loads once per version.
scoreboard objectives add hrRigC dummy
scoreboard objectives add hrRigT dummy
scoreboard objectives add hrRigF dummy
scoreboard objectives add hrRigY dummy
scoreboard objectives add hrRigS dummy
scoreboard objectives add hrRigForm dummy
scoreboard objectives add hrRigPh dummy
scoreboard objectives add hrRigBl dummy
scoreboard objectives add hrRigFc dummy
scoreboard objectives add hrRigHR dummy
scoreboard objectives add hrRigHL dummy
scoreboard objectives add hrRigHat dummy
scoreboard objectives add hrRigSw dummy
scoreboard objectives add hrRigSc dummy
scoreboard objectives add hrRigPr dummy
scoreboard objectives add hrRigCu dummy
scoreboard objectives add hrRigBo dummy
scoreboard objectives add hrRigQ dummy
scoreboard objectives add hrRigQx dummy
scoreboard objectives add hrRigQy dummy
scoreboard objectives add hrRigQz dummy
scoreboard objectives add hrRigQw dummy
execute unless data storage rlk:hr rig{anv:173603159} run function rlk:boss/scarlet/rig/an/load
