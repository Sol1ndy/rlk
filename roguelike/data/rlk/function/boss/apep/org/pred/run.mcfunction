# @s = a 포식성: 1 seek a basic, 2 swallow -> bud -> inflate -> burst (O6a), 4 circle the player 3-5 b, 6 a bite chain (O6b,
# apSock 1 / 2), 7 a single bite, 9 the gap before chain 2. The fish hovers 1.2 b up (the model).
execute if score @s apS matches 1 run return run function rlk:boss/apep/org/pred/seek
execute if score @s apS matches 2 run return run function rlk:boss/apep/org/pred/swallow
execute if score @s apS matches 6 run return run function rlk:boss/apep/org/pred/chain
execute if score @s apS matches 7 run return run function rlk:boss/apep/org/pred/single
execute if score @s apS matches 9 run return run function rlk:boss/apep/org/pred/gap
function rlk:boss/apep/org/pred/circle
