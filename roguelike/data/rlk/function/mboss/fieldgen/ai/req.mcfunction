# A test request (#fgReq = pattern id): the device state follows the pattern at once.
scoreboard players operation #fgPick mb = #fgReq mb
scoreboard players set #fgReq mb 0
scoreboard players operation #fgLast mb = #fgPick mb
execute if score #fgPick mb matches 1 if score #fgField mb matches 1.. run function rlk:mboss/fieldgen/field/now_c
execute if score #fgPick mb matches 2 if score #fgField mb matches 1.. run function rlk:mboss/fieldgen/field/now_c
execute if score #fgPick mb matches 3 if score #fgField mb matches 1.. run function rlk:mboss/fieldgen/field/now_c
execute if score #fgPick mb matches 4 if score #fgField mb matches 1.. run function rlk:mboss/fieldgen/field/now_c
execute if score #fgPick mb matches 5 if score #fgField mb matches 1.. run function rlk:mboss/fieldgen/field/now_c
execute if score #fgPick mb matches 6 if score #fgField mb matches 1.. run function rlk:mboss/fieldgen/field/now_c
execute if score #fgPick mb matches 20 if score #fgField mb matches 1.. run function rlk:mboss/fieldgen/field/now_c
execute if score #fgPick mb matches 11 unless score #fgField mb matches 3 run function rlk:mboss/fieldgen/field/now_f
execute if score #fgPick mb matches 12 unless score #fgField mb matches 3 run function rlk:mboss/fieldgen/field/now_f
execute if score #fgPick mb matches 21..22 run function rlk:mboss/fieldgen/field/now_f
execute if score #fgPick mb matches 21 run scoreboard players operation #fgWvK mb = #fgReqK mb
execute if score #fgPick mb matches 21 if score #fgWvK mb matches 1 run scoreboard players set #fgField mb 2
execute if score #fgPick mb matches 21 if score #fgWvK mb matches 2 run scoreboard players set #fgField mb 4
execute if score #fgPick mb matches 22 run scoreboard players set #fgField mb 5
function rlk:mboss/fieldgen/ai/go
