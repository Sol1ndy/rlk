# G1 swap (@s = body): 24 t standing; she drags the blade through her palm, the edge changes at tick 14.
scoreboard players set #pat tk 50
scoreboard players set #pt tk 0
scoreboard players set #done tk 0
execute if score #el tk matches 1 run function rlk:boss/tachy/rig/play/swap_electro
execute if score #el tk matches 3 run function rlk:boss/tachy/rig/play/swap_pyro
execute if score #el tk matches 1 run function rlk:boss/tachy/fx/snd/swap_electro
execute if score #el tk matches 3 run function rlk:boss/tachy/fx/snd/swap_pyro
function rlk:boss/tachy/hud/sub
