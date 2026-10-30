# The visor look: the abyss skull from T2 on, else the current element (@s = body).
execute if score #ph tk matches 6.. run return run function rlk:boss/tachy/rig/look/visor/down_abyss
execute if score #el tk matches 1 run function rlk:boss/tachy/rig/look/visor/down_pyro
execute if score #el tk matches 3 run function rlk:boss/tachy/rig/look/visor/down_electro
