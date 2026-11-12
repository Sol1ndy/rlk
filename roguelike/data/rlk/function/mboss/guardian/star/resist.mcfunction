# Own-element hit on an active star: 40 % RES (x0.6, at least 1 so a light hit still
# shows a number). Replaces the source's immunity (user decision).
execute if score #dmg tmp matches ..0 run return 0
scoreboard players set #gdX mb 60
scoreboard players operation #dmg tmp *= #gdX mb
scoreboard players operation #dmg tmp /= #c100 mb
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
