# Stand-in t2 tick (#sq tk 1..110).
execute if score #sq tk matches 20 run function rlk:boss/tachy/rig_stub/look/visor/down_abyss
execute if score #sq tk matches 50 run effect give @a[tag=player] minecraft:blindness 1 0 true
execute if score #sq tk matches 60 run function rlk:boss/tachy/rig_stub/look/form/abyss
execute if score #sq tk matches 110.. run scoreboard players set #sqdone tk 1
