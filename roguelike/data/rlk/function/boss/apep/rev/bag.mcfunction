# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# One special from the shuffle bag ['guard', 'nest', 'nurt', 'pred'] (each once before any repeats; #apBg<i> 1 = drawn).
execute if score #apBg0 mb matches 1 if score #apBg1 mb matches 1 if score #apBg2 mb matches 1 if score #apBg3 mb matches 1 run function rlk:boss/apep/rev/bag_fill
execute store result score #apR mb run random value 0..3
execute if score #apR mb matches 0 if score #apBg0 mb matches 0 run return run function rlk:boss/apep/rev/bag_0
execute if score #apR mb matches 0 if score #apBg1 mb matches 0 run return run function rlk:boss/apep/rev/bag_1
execute if score #apR mb matches 0 if score #apBg2 mb matches 0 run return run function rlk:boss/apep/rev/bag_2
execute if score #apR mb matches 0 if score #apBg3 mb matches 0 run return run function rlk:boss/apep/rev/bag_3
execute if score #apR mb matches 1 if score #apBg1 mb matches 0 run return run function rlk:boss/apep/rev/bag_1
execute if score #apR mb matches 1 if score #apBg2 mb matches 0 run return run function rlk:boss/apep/rev/bag_2
execute if score #apR mb matches 1 if score #apBg3 mb matches 0 run return run function rlk:boss/apep/rev/bag_3
execute if score #apR mb matches 1 if score #apBg0 mb matches 0 run return run function rlk:boss/apep/rev/bag_0
execute if score #apR mb matches 2 if score #apBg2 mb matches 0 run return run function rlk:boss/apep/rev/bag_2
execute if score #apR mb matches 2 if score #apBg3 mb matches 0 run return run function rlk:boss/apep/rev/bag_3
execute if score #apR mb matches 2 if score #apBg0 mb matches 0 run return run function rlk:boss/apep/rev/bag_0
execute if score #apR mb matches 2 if score #apBg1 mb matches 0 run return run function rlk:boss/apep/rev/bag_1
execute if score #apR mb matches 3 if score #apBg3 mb matches 0 run return run function rlk:boss/apep/rev/bag_3
execute if score #apR mb matches 3 if score #apBg0 mb matches 0 run return run function rlk:boss/apep/rev/bag_0
execute if score #apR mb matches 3 if score #apBg1 mb matches 0 run return run function rlk:boss/apep/rev/bag_1
execute if score #apR mb matches 3 if score #apBg2 mb matches 0 run return run function rlk:boss/apep/rev/bag_2
