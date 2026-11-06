# @s = player: exactly one level: #xpAdd = xpNeed - xp (at least 1) through player/level/add_xp (the normal level-up:
# fanfare, stats, pkPending +1 = its usual item pick).
scoreboard players operation #xpAdd tmp = @s xpNeed
scoreboard players operation #xpAdd tmp -= @s xp
execute if score #xpAdd tmp matches ..0 run scoreboard players set #xpAdd tmp 1
function rlk:player/level/add_xp
