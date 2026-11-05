# A gauntlet tick (@s = body): #pt + 1, p/<g>/tick (or the stand-in), the pip windows (shield/tick), its end.
scoreboard players add #pt hr 1
execute if score #pat hr matches 21 run function rlk:boss/scarlet/core/gs/a8/tick
execute if score #pat hr matches 27 run function rlk:boss/scarlet/core/gs/a13/tick
function rlk:boss/scarlet/shield/tick
execute if score #done hr matches 1 run function rlk:boss/scarlet/core/g/end
