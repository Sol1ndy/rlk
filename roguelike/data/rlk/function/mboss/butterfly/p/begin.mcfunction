# @s = body. First tick of the slot pattern #bfPat: clock -lead (0 for most), the clip at clock 0, start.
scoreboard players set #bfPNew mb 0
scoreboard players set #bfPT mb 0
scoreboard players set #bfPEnd mb 0
scoreboard players set #bfPRel mb 0
scoreboard players set #bfPMax mb 200
scoreboard players set #bfPLen mb 200
scoreboard players set #bfPCol mb 8
execute if score #bfPat mb matches 1 run scoreboard players set #bfPMax mb 56
execute if score #bfPat mb matches 2 run scoreboard players set #bfPMax mb 70
execute if score #bfPat mb matches 3 run scoreboard players set #bfPMax mb 55
execute if score #bfPat mb matches 4 run scoreboard players set #bfPMax mb 46
execute if score #bfPat mb matches 11 run scoreboard players set #bfPMax mb 60
execute if score #bfPat mb matches 12 run scoreboard players set #bfPMax mb 189
execute if score #bfPat mb matches 13 run scoreboard players set #bfPMax mb 64
execute if score #bfPat mb matches 14 run scoreboard players set #bfPMax mb 102
execute if score #bfPat mb matches 15 run scoreboard players set #bfPMax mb 100
execute if score #bfPat mb matches 20 run scoreboard players set #bfPMax mb 34
# expected end for the progress bar (a pattern that decides a shorter run sets #bfPLen itself: g.set_len)
execute if score #bfPat mb matches 1 run scoreboard players set #bfPLen mb 51
execute if score #bfPat mb matches 2 run scoreboard players set #bfPLen mb 65
execute if score #bfPat mb matches 3 run scoreboard players set #bfPLen mb 50
execute if score #bfPat mb matches 4 run scoreboard players set #bfPLen mb 41
execute if score #bfPat mb matches 11 run scoreboard players set #bfPLen mb 55
execute if score #bfPat mb matches 12 run scoreboard players set #bfPLen mb 117
execute if score #bfPat mb matches 13 run scoreboard players set #bfPLen mb 59
execute if score #bfPat mb matches 14 run scoreboard players set #bfPLen mb 98
execute if score #bfPat mb matches 15 run scoreboard players set #bfPLen mb 96
execute if score #bfPat mb matches 20 run scoreboard players set #bfPLen mb 30
execute if score #bfPat mb matches 1 run scoreboard players set #bfPCol mb 7
execute if score #bfPat mb matches 2 run scoreboard players set #bfPCol mb 7
execute if score #bfPat mb matches 3 run scoreboard players set #bfPCol mb 7
execute if score #bfPat mb matches 4 run scoreboard players set #bfPCol mb 7
execute if score #bfPat mb matches 11 run scoreboard players set #bfPCol mb 7
execute if score #bfPat mb matches 12 run scoreboard players set #bfPCol mb 2
execute if score #bfPat mb matches 13 run scoreboard players set #bfPCol mb 2
execute if score #bfPat mb matches 14 run scoreboard players set #bfPCol mb 7
execute if score #bfPat mb matches 15 run scoreboard players set #bfPCol mb 7
execute if score #bfPat mb matches 20 run scoreboard players set #bfPCol mb 7
execute if score #bfPat mb matches 1 run scoreboard players set #bfPT mb -2
function rlk:mboss/butterfly/hud/refresh
execute if score #bfPT mb matches 0 run function rlk:mboss/butterfly/p/clip_d
function rlk:mboss/butterfly/p/start
execute if score #bfPat mb matches 15.. run function rlk:mboss/butterfly/p/svc
