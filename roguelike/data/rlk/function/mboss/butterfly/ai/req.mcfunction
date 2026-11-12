# A test request (#bfReq = pattern id): the form follows the pattern at once (no transformation).
scoreboard players operation #bfPick mb = #bfReq mb
scoreboard players set #bfReq mb 0
# no immediate repeat after a requested pattern either (the forced H2 after the groggy)
scoreboard players operation #bfLast mb = #bfPick mb
execute if score #bfPick mb matches 1 if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/now_h
execute if score #bfPick mb matches 2 if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/now_h
execute if score #bfPick mb matches 3 if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/now_h
execute if score #bfPick mb matches 4 if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/now_h
execute if score #bfPick mb matches 11 if score #bfForm mb matches 1 run function rlk:mboss/butterfly/form/now_b
execute if score #bfPick mb matches 12 if score #bfForm mb matches 1 run function rlk:mboss/butterfly/form/now_b
execute if score #bfPick mb matches 13 if score #bfForm mb matches 1 run function rlk:mboss/butterfly/form/now_b
execute if score #bfPick mb matches 14 if score #bfForm mb matches 1 run function rlk:mboss/butterfly/form/now_b
execute if score #bfPick mb matches 15 if score #bfForm mb matches 1 run function rlk:mboss/butterfly/form/now_b
execute if score #bfPick mb matches 20 if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/now_h
function rlk:mboss/butterfly/ai/launch
