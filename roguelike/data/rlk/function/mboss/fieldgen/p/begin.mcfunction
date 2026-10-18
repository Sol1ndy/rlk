# @s = body. First tick of the slot pattern #fgPat: clock -lead (0 for most), the clip at clock 0, start.
scoreboard players set #fgPNew mb 0
scoreboard players set #fgPT mb 0
scoreboard players set #fgPEnd mb 0
scoreboard players set #fgPRel mb 0
scoreboard players set #fgPMax mb 200
scoreboard players set #fgPLen mb 200
scoreboard players set #fgPCol mb 5
execute if score #fgPat mb matches 1 run scoreboard players set #fgPMax mb 110
execute if score #fgPat mb matches 2 run scoreboard players set #fgPMax mb 52
execute if score #fgPat mb matches 3 run scoreboard players set #fgPMax mb 180
execute if score #fgPat mb matches 4 run scoreboard players set #fgPMax mb 78
execute if score #fgPat mb matches 5 run scoreboard players set #fgPMax mb 118
execute if score #fgPat mb matches 6 run scoreboard players set #fgPMax mb 165
execute if score #fgPat mb matches 11 run scoreboard players set #fgPMax mb 268
execute if score #fgPat mb matches 12 run scoreboard players set #fgPMax mb 118
execute if score #fgPat mb matches 21 run scoreboard players set #fgPMax mb 232
execute if score #fgPat mb matches 20 run scoreboard players set #fgPMax mb 62
execute if score #fgPat mb matches 22 run scoreboard players set #fgPMax mb 83
# expected end for the progress bar (a pattern that decides a shorter run sets #fgPLen itself: g.set_len)
execute if score #fgPat mb matches 1 run scoreboard players set #fgPLen mb 100
execute if score #fgPat mb matches 2 run scoreboard players set #fgPLen mb 45
execute if score #fgPat mb matches 3 run scoreboard players set #fgPLen mb 174
execute if score #fgPat mb matches 4 run scoreboard players set #fgPLen mb 70
execute if score #fgPat mb matches 5 run scoreboard players set #fgPLen mb 110
execute if score #fgPat mb matches 6 run scoreboard players set #fgPLen mb 157
execute if score #fgPat mb matches 11 run scoreboard players set #fgPLen mb 260
execute if score #fgPat mb matches 12 run scoreboard players set #fgPLen mb 110
execute if score #fgPat mb matches 21 run scoreboard players set #fgPLen mb 212
execute if score #fgPat mb matches 20 run scoreboard players set #fgPLen mb 57
execute if score #fgPat mb matches 22 run scoreboard players set #fgPLen mb 78
function rlk:mboss/fieldgen/hud/refresh
execute if score #fgPT mb matches 0 run function rlk:mboss/fieldgen/p/clip_d
function rlk:mboss/fieldgen/p/start
execute if score #fgPat mb matches 20.. run function rlk:mboss/fieldgen/p/svc
