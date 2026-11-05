# The running pattern of a fight phase (@s = body): #pt + 1, p/<key>/tick, its end.
scoreboard players add #pt hr 1
execute if score #pat hr matches 1 run function rlk:boss/scarlet/p/a1/tick
execute if score #pat hr matches 2 run function rlk:boss/scarlet/p/a2/tick
execute if score #pat hr matches 3 run function rlk:boss/scarlet/p/a3/tick
execute if score #pat hr matches 4 run function rlk:boss/scarlet/p/a4/tick
execute if score #pat hr matches 5 run function rlk:boss/scarlet/p/a6/tick
execute if score #pat hr matches 6 run function rlk:boss/scarlet/p/a9/tick
execute if score #pat hr matches 7 run function rlk:boss/scarlet/p/a10/tick
execute if score #done hr matches 1 run function rlk:boss/scarlet/core/pat_end
