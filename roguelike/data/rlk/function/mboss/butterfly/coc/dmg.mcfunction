# Player DMG on the body x #bfDmgPct % (50 under 달빛 고치; 100 otherwise: the reward is crit, not damage), at least 1.
scoreboard players operation #dmg tmp *= #bfDmgPct mb
scoreboard players operation #dmg tmp /= #c100 mb
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
