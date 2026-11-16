# The FLANK rule (plan 4.12): dwell >= 4 of 6 samples in FLANK-near, or a flank proxy hit in the last 40 t; then
# 90 %: not after P6 -> P6; after P6 with the player still in FLANK-near or TAIL-off -> P7 (anchor8 + an
# exit), else P8 (TAIL-off, anchor8) or P2. The other 10 % use the FLANK-near column. Returns 1 when it picked.
scoreboard players set #azX mb 0
execute if score #azDwell mb matches 4.. run scoreboard players set #azX mb 1
execute if score #azPxF mb matches 1 run scoreboard players set #azX mb 1
execute if score #azX mb matches 0 run return fail
execute store result score #azR mb run random value 0..99
execute if score #azR mb matches 90.. run return run function rlk:boss/azhdaha/ai/flank_col
execute unless score #azLast mb matches 6 run return run function rlk:boss/azhdaha/ai/flank_p6
scoreboard players set #azX mb 0
execute if score #azFN mb matches 1 run scoreboard players set #azX mb 1
execute if score #azZone mb matches 7 run scoreboard players set #azX mb 1
execute if score #azX mb matches 0 run return fail
execute if score #azA8 mb matches 1 if score #azExit mb matches 1 run return run function rlk:boss/azhdaha/ai/flank_p7
execute if score #azA8 mb matches 1 if score #azZone mb matches 7 run return run function rlk:boss/azhdaha/ai/flank_p8
return run function rlk:boss/azhdaha/ai/flank_p2
