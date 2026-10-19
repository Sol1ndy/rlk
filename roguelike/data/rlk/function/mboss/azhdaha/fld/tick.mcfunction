# @s = body: the field table: a field whose end tick passed is freed (its hazard expires by itself).
execute if score #azF0 mb matches 1.. if score #azClk mb >= #azFE0 mb run function rlk:mboss/azhdaha/fld/cancel_0
execute if score #azF1 mb matches 1.. if score #azClk mb >= #azFE1 mb run function rlk:mboss/azhdaha/fld/cancel_1
execute if score #azF2 mb matches 1.. if score #azClk mb >= #azFE2 mb run function rlk:mboss/azhdaha/fld/cancel_2
execute if score #azF3 mb matches 1.. if score #azClk mb >= #azFE3 mb run function rlk:mboss/azhdaha/fld/cancel_3
execute if score #azF4 mb matches 1.. if score #azClk mb >= #azFE4 mb run function rlk:mboss/azhdaha/fld/cancel_4
execute if score #azF5 mb matches 1.. if score #azClk mb >= #azFE5 mb run function rlk:mboss/azhdaha/fld/cancel_5
execute if score #azF6 mb matches 1.. if score #azClk mb >= #azFE6 mb run function rlk:mboss/azhdaha/fld/cancel_6
execute if score #azF7 mb matches 1.. if score #azClk mb >= #azFE7 mb run function rlk:mboss/azhdaha/fld/cancel_7
execute unless score #azF0 mb matches 1 unless score #azF1 mb matches 1 unless score #azF2 mb matches 1 unless score #azF3 mb matches 1 unless score #azF4 mb matches 1 unless score #azF5 mb matches 1 unless score #azF6 mb matches 1 unless score #azF7 mb matches 1 run scoreboard players set #azFG1 mb 0
execute unless score #azF0 mb matches 2 unless score #azF1 mb matches 2 unless score #azF2 mb matches 2 unless score #azF3 mb matches 2 unless score #azF4 mb matches 2 unless score #azF5 mb matches 2 unless score #azF6 mb matches 2 unless score #azF7 mb matches 2 run scoreboard players set #azFG2 mb 0
execute unless score #azF0 mb matches 3 unless score #azF1 mb matches 3 unless score #azF2 mb matches 3 unless score #azF3 mb matches 3 unless score #azF4 mb matches 3 unless score #azF5 mb matches 3 unless score #azF6 mb matches 3 unless score #azF7 mb matches 3 run scoreboard players set #azFG3 mb 0
