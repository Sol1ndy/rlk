# Stand-in intro tick (#sq tk 1..184).
execute if score #sq tk matches 126 run function rlk:boss/tachy/rig_stub/look/visor/down_pyro
execute if score #sq tk matches 156 run function rlk:boss/tachy/rig_stub/look/edge/pyro
execute if score #sq tk matches 156 run title @a[tag=player] times 6 40 12
execute if score #sq tk matches 156 run title @a[tag=player] subtitle ["",{text:"잠식된 제7공수대원",color:"#E8E2D0"}]
execute if score #sq tk matches 156 run title @a[tag=player] title ["",{text:"타키",color:"#F2C230",bold:true}]
execute if score #sq tk matches 184.. run scoreboard players set #sqdone tk 1
