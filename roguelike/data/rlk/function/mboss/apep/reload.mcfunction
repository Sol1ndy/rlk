# Hook reload (@s = body after /reload: every rlk_mb_aux entity is gone: the rig parts, hazards, organisms, the
# Heart, domes, walls' markers, props, proxies). Scores survive; the state is re-derived from them (plan 7.2):
#   E -> the end of E; P1 -> the rig again, the pattern cancelled; T1 -> phase 2 ready; P2 -> the stage keeps its
#   progress / wave / clock / strikes, the Heart and the wave again, parked; CS -> phase 3 ready; P3 -> the rig
#   again (UPRIGHT), the pattern cancelled, a running Q2 cancelled (300 t).
function rlk:mboss/apep/ai/consts
scoreboard players set #apHide mb -1
execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
function rlk:mboss/apep/rig/init
function rlk:mboss/apep/rig/spawn
execute if score #apPid mb matches 32 run function rlk:mboss/apep/aft/cancel
execute if score #mbSt mb matches 0 run return run function rlk:mboss/apep/intro/done
execute if score #apPh mb matches 15 run return run function rlk:mboss/apep/ph/ready_2
execute if score #apPh mb matches 25 run return run function rlk:mboss/apep/ph/ready_3
execute if score #apPh mb matches 2 run return run function rlk:mboss/apep/rl/p2
execute if score #apPh mb matches 3 run return run function rlk:mboss/apep/rl/p3
function rlk:mboss/apep/rl/p1
