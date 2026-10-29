# Stand-in t1 tick (#sq tk 1..80).
execute if score #sq tk matches 10 run function rlk:boss/tachy/rig_stub/look/form/winged
execute if score #sq tk matches 80.. run scoreboard players set #sqdone tk 1
