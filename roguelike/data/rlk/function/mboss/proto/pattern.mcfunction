# @s = body: the running pattern (#prGo = still closing in; the clock waits at 0).
execute if score #prGo mb matches 1 run return run function rlk:mboss/proto/close_in
scoreboard players add #prT mb 1
execute if score #prPat mb matches 1 run function rlk:mboss/proto/p/1
execute if score #prPat mb matches 2 run function rlk:mboss/proto/p/2
execute if score #prPat mb matches 3 run function rlk:mboss/proto/p/3
execute if score #prPat mb matches 4 run function rlk:mboss/proto/p/4
execute if score #prPat mb matches 5 run function rlk:mboss/proto/p/5
execute if score #prPat mb matches 6 run function rlk:mboss/proto/p/6
execute if score #prPat mb matches 7 run function rlk:mboss/proto/p/7
