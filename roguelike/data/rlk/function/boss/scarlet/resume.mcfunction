# Hook resume (@s = body): a pattern's own resume; a pending gauntlet restart (#grs).
execute if score #grs hr matches 1 if score #gk hr matches 1 run function rlk:boss/scarlet/core/lead/a8
execute if score #grs hr matches 1 if score #gk hr matches 2 run function rlk:boss/scarlet/core/lead/a13
execute if score #grs hr matches 2 run function rlk:boss/scarlet/core/revive/start
execute if score #grs hr matches 3 run function rlk:boss/scarlet/core/repel/start
execute if score #grs hr matches 1 run scoreboard players set #sq hr -1
execute if score #grs hr matches 3 run scoreboard players set #sq hr -1
scoreboard players set #grs hr 0
