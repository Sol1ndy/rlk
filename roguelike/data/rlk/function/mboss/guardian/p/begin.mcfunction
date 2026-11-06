# @s = body. First tick of the slot pattern #gdPat: clock 0, start function (plays its clip).
scoreboard players set #gdPNew mb 0
scoreboard players set #gdPT mb 0
scoreboard players set #gdPEnd mb 0
scoreboard players set #gdPRel mb 0
scoreboard players set #gdPMax mb 200
scoreboard players set #gdPLen mb 200
execute if score #gdPat mb matches 1 run scoreboard players set #gdPMax mb 83
execute if score #gdPat mb matches 2 run scoreboard players set #gdPMax mb 71
execute if score #gdPat mb matches 3 run scoreboard players set #gdPMax mb 68
execute if score #gdPat mb matches 4 run scoreboard players set #gdPMax mb 86
execute if score #gdPat mb matches 5 run scoreboard players set #gdPMax mb 95
execute if score #gdPat mb matches 11 run scoreboard players set #gdPMax mb 43
execute if score #gdPat mb matches 12 run scoreboard players set #gdPMax mb 49
execute if score #gdPat mb matches 13 run scoreboard players set #gdPMax mb 100
# expected end for the progress bar (a pattern that decides a shorter run sets #gdPLen itself: g.set_len)
execute if score #gdPat mb matches 1 run scoreboard players set #gdPLen mb 79
execute if score #gdPat mb matches 2 run scoreboard players set #gdPLen mb 67
execute if score #gdPat mb matches 3 run scoreboard players set #gdPLen mb 64
execute if score #gdPat mb matches 4 run scoreboard players set #gdPLen mb 82
execute if score #gdPat mb matches 5 run scoreboard players set #gdPLen mb 91
execute if score #gdPat mb matches 11 run scoreboard players set #gdPLen mb 39
execute if score #gdPat mb matches 12 run scoreboard players set #gdPLen mb 45
execute if score #gdPat mb matches 13 run scoreboard players set #gdPLen mb 91
execute if score #gdSt mb matches 1 run function rlk:mboss/guardian/hud/sub_pattern
function rlk:mboss/guardian/p/start
