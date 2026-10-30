# The gap closer one tick (#pat 56, @s = body): gone at 6, back beside / behind the player at
# 10, the queued chain at 14.
scoreboard players add #pt tk 1
execute if score #pt tk matches 6 run function rlk:boss/tachy/core/close/out
execute if score #pt tk matches 10 run function rlk:boss/tachy/core/close/in
execute if score #pt tk matches 11..13 run function rlk:mboss/mv/turn {max:30}
execute if score #pt tk matches 14.. run function rlk:boss/tachy/core/close/go
