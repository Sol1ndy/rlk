# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# The current wave #apWave (also /reload: the wave again): 4 basics on 4 of the 8 r 12 points (odd / even by
# the wave; wave 1: 2 melee + 2 ranged, later 50 / 50), then its specials (waves 2-5 the table, 6 one from the bag,
# 7+ two).
scoreboard players set #apOArg mb -1
execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb 0
scoreboard players operation #apM mb = #apWave mb
scoreboard players operation #apM mb %= #apK2 mb
execute if score #apM mb matches 1 positioned 444.59 201 -3.09 run function rlk:boss/apep/org/spawn_basic
scoreboard players set #apOArg mb -1
execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb 1
scoreboard players operation #apM mb = #apWave mb
scoreboard players operation #apM mb %= #apK2 mb
execute if score #apM mb matches 1 positioned 451.09 201 12.59 run function rlk:boss/apep/org/spawn_basic
scoreboard players set #apOArg mb -1
execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb 0
scoreboard players operation #apM mb = #apWave mb
scoreboard players operation #apM mb %= #apK2 mb
execute if score #apM mb matches 1 positioned 435.41 201 19.09 run function rlk:boss/apep/org/spawn_basic
scoreboard players set #apOArg mb -1
execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb 1
scoreboard players operation #apM mb = #apWave mb
scoreboard players operation #apM mb %= #apK2 mb
execute if score #apM mb matches 1 positioned 428.91 201 3.41 run function rlk:boss/apep/org/spawn_basic
scoreboard players set #apOArg mb -1
execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb 0
scoreboard players operation #apM mb = #apWave mb
scoreboard players operation #apM mb %= #apK2 mb
execute if score #apM mb matches 0 positioned 451.09 201 3.41 run function rlk:boss/apep/org/spawn_basic
scoreboard players set #apOArg mb -1
execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb 1
scoreboard players operation #apM mb = #apWave mb
scoreboard players operation #apM mb %= #apK2 mb
execute if score #apM mb matches 0 positioned 444.59 201 19.09 run function rlk:boss/apep/org/spawn_basic
scoreboard players set #apOArg mb -1
execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb 0
scoreboard players operation #apM mb = #apWave mb
scoreboard players operation #apM mb %= #apK2 mb
execute if score #apM mb matches 0 positioned 428.91 201 12.59 run function rlk:boss/apep/org/spawn_basic
scoreboard players set #apOArg mb -1
execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb 1
scoreboard players operation #apM mb = #apWave mb
scoreboard players operation #apM mb %= #apK2 mb
execute if score #apM mb matches 0 positioned 435.41 201 -3.09 run function rlk:boss/apep/org/spawn_basic
execute if score #apWave mb matches 2 run function rlk:boss/apep/rev/sp_guard
execute if score #apWave mb matches 3 run function rlk:boss/apep/rev/sp_nest
execute if score #apWave mb matches 4 run function rlk:boss/apep/rev/sp_nurt
execute if score #apWave mb matches 5 run function rlk:boss/apep/rev/sp_pred
execute if score #apWave mb matches 6.. run function rlk:boss/apep/rev/sp_bag
execute if score #apWave mb matches 7.. run function rlk:boss/apep/rev/sp_bag
