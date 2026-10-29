# Transition tick (#pat 54): the sequence on #sq; T1 push ring (no damage) at its flare, T2 music phase 2 at its swap.
scoreboard players add #sq tk 1
execute if score #ph tk matches 3 run function rlk:boss/tachy/core/sq/t1/tick
execute if score #ph tk matches 6 run function rlk:boss/tachy/core/sq/t2/tick
execute if score #ph tk matches 3 if score #sq tk matches 50 at @s run function rlk:mboss/push/ring {r:40,to:45,kb:4}
execute if score #ph tk matches 6 if score #sq tk matches 60 run function rlk:mboss/music/set {ph:2}
execute if score #sqdone tk matches 1 run return run function rlk:boss/tachy/core/tr/end
execute if score #ph tk matches 3 if score #sq tk matches 120.. run return run function rlk:boss/tachy/core/tr/end
execute if score #ph tk matches 6 if score #sq tk matches 150.. run function rlk:boss/tachy/core/tr/end
