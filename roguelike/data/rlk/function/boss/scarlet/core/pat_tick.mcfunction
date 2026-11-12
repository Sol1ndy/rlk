# The running pattern of a fight phase (@s = body): #pt + 1, p/<key>/tick (or the perfect-parry flinch), its end.
scoreboard players add #pt hr 1
execute if score #ppf hr matches 1.. run return run function rlk:boss/scarlet/core/ppf
execute if score #pat hr matches 1 run function rlk:boss/scarlet/p/a1/tick
execute if score #pat hr matches 2 run function rlk:boss/scarlet/p/a2/tick
execute if score #pat hr matches 3 run function rlk:boss/scarlet/p/a3/tick
execute if score #pat hr matches 4 run function rlk:boss/scarlet/p/a4/tick
execute if score #pat hr matches 5 run function rlk:boss/scarlet/p/a6/tick
execute if score #pat hr matches 6 run function rlk:boss/scarlet/p/a9/tick
execute if score #pat hr matches 7 run function rlk:boss/scarlet/p/a10/tick
execute if score #pat hr matches 8 run function rlk:boss/scarlet/p/a3s/tick
execute if score #pat hr matches 9 run function rlk:boss/scarlet/p/d4/tick
execute if score #pat hr matches 10 run function rlk:boss/scarlet/p/tri/tick
execute if score #pat hr matches 11 run function rlk:boss/scarlet/p/rings/tick
execute if score #pat hr matches 12 run function rlk:boss/scarlet/p/ult/tick
execute if score #pat hr matches 13 run function rlk:boss/scarlet/p/hcut/tick
execute if score #pat hr matches 14 run function rlk:boss/scarlet/p/blue/tick
execute if score #pat hr matches 15 run function rlk:boss/scarlet/p/kcut/tick
execute if score #pat hr matches 16 run function rlk:boss/scarlet/p/mx/tick
execute if score #pat hr matches 17 run function rlk:boss/scarlet/p/nb/tick
execute if score #pat hr matches 18 run function rlk:boss/scarlet/p/q/tick
execute if score #done hr matches 1 run function rlk:boss/scarlet/core/pat_end
