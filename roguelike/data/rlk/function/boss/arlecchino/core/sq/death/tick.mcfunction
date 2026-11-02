# Stand-in death tick (#sq kn 1..110).
execute if score #sq kn matches 30 run function rlk:boss/arlecchino/rig_stub/look/weapon_r/gone
execute if score #sq kn matches 30 run function rlk:boss/arlecchino/rig_stub/look/weapon_l/gone
execute if score #sq kn matches 96 run function rlk:boss/arlecchino/rig_stub/state/hidden
execute if score #sq kn matches 110.. run scoreboard players set #sqdone kn 1
