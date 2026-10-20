# slide tick (#azPT; the clip tick = #azPT - 40).
execute if score #azPT mb matches ..39 run scoreboard players set #azNoPush mb 1
execute if score #azPT mb matches ..39 if score #aq20M mb matches 1 run function rlk:mboss/mv/turn {max:4}
execute if score #azPT mb matches ..39 if score #aq20M mb matches 0 run function rlk:mboss/mv/turn {max:1}
execute if score #azPT mb matches ..39 if score #aq20M mb matches 1 if score #azPT mb = #aq20G mb run function rlk:mboss/azhdaha/rig/play/walk_stop
execute if score #azPT mb matches 40.. run scoreboard players set #azNoTurn mb 1
execute if score #azPT mb matches 40..143 run return run function rlk:mboss/azhdaha/p/slide/kd/40_143
execute if score #azPT mb matches 144..243 run return run function rlk:mboss/azhdaha/p/slide/kd/144_243
