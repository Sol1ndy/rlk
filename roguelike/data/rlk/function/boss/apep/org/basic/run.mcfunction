# @s = a basic: 1 walk to the Heart, 2 to its socket, 3 wait on the ring, 4 melee loop, 5 lying down, 6 lying (no slot),
# 7 the ranged loop, 8 held by a 포식성. Never chases the player.
execute if score @s apS matches 4 run return run function rlk:boss/apep/org/basic/melee
execute if score @s apS matches 7 run return run function rlk:boss/apep/org/basic/fire
execute if score @s apS matches 1 run return run function rlk:boss/apep/org/basic/walk
execute if score @s apS matches 2 run return run function rlk:boss/apep/org/basic/sock
execute if score @s apS matches 3 run return run function rlk:boss/apep/org/basic/wait
execute if score @s apS matches 5 run return run function rlk:boss/apep/org/basic/lie
execute if score @s apS matches 6 run return run function rlk:boss/apep/org/basic/ridle
