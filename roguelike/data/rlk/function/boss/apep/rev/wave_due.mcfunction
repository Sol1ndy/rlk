# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# The next wave: due when <= 1 alive or 600 t after the last; it waits
# while alive + its size > the cap 6.
scoreboard players set #apX mb 0
execute if score #apWT mb matches 600.. run scoreboard players set #apX mb 1
execute if score #apAlive mb matches ..1 run scoreboard players set #apX mb 1
execute if score #apX mb matches 0 run return 0
scoreboard players set #apY mb 4
execute if score #apWave mb matches 1.. run scoreboard players set #apY mb 5
execute if score #apWave mb matches 6.. run scoreboard players set #apY mb 6
scoreboard players operation #apY mb += #apAlive mb
execute if score #apY mb matches 7.. run return 0
scoreboard players add #apWave mb 1
scoreboard players set #apWT mb 0
scoreboard players set #apHudQ mb 1
function rlk:boss/apep/rev/wave_spawn
