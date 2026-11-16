scoreboard players operation #dmg tmp *= #fgCut mb
scoreboard players operation #dmg tmp /= #c100 mb
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
