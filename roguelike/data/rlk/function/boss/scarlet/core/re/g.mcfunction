# /reload in a gauntlet: as a pause (cancelled, the darkness lifted), then at once its restart (F1: or P2 after
# the judged A8 fail; a pending lethal fail lands now when the player is back and alive, else at the resume).
function rlk:boss/scarlet/core/g/pause
execute if score #grs hr matches 1 if score #gk hr matches 1 run function rlk:boss/scarlet/core/lead/re_a8
execute if score #grs hr matches 1 if score #gk hr matches 2 run function rlk:boss/scarlet/core/lead/re_a13
execute if score #grs hr matches 2 run function rlk:boss/scarlet/core/revive/start
execute if score #grs hr matches 3 run function rlk:boss/scarlet/core/repel/start
execute if score #grs hr matches 4 run function rlk:boss/scarlet/core/p2/from_fail
execute if score #grs hr matches 5 if entity @a[tag=player,limit=1] unless entity @a[tag=player,scores={dead=1}] unless entity @a[tag=player,scores={rnDie=1..}] run function rlk:boss/scarlet/core/g/fail_now
execute if score #grs hr matches 1 run scoreboard players set #sq hr -1
execute if score #grs hr matches 3 run scoreboard players set #sq hr -1
execute unless score #grs hr matches 5 run scoreboard players set #grs hr 0
