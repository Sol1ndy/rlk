scoreboard players set #inM view 0
execute if predicate rlk:in_f run scoreboard players add #inM view 1
execute if predicate rlk:in_b run scoreboard players add #inM view 2
execute if predicate rlk:in_l run scoreboard players add #inM view 4
execute if predicate rlk:in_r run scoreboard players add #inM view 8
execute if predicate rlk:in_jump run scoreboard players add #inM view 16
execute if predicate rlk:in_sprint run scoreboard players add #inM view 32
execute unless score #inM view = #inBase view run scoreboard players set #inStale view 0
