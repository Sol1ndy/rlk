# Cancel the oldest live field of the new field's family (lowest sequence).
scoreboard players set #azX mb 2147483647
scoreboard players set #azY mb -1
execute if score #azF0 mb = #azNfF mb if score #azFS0 mb < #azX mb run scoreboard players set #azY mb 0
execute if score #azF0 mb = #azNfF mb if score #azFS0 mb < #azX mb run scoreboard players operation #azX mb = #azFS0 mb
execute if score #azF1 mb = #azNfF mb if score #azFS1 mb < #azX mb run scoreboard players set #azY mb 1
execute if score #azF1 mb = #azNfF mb if score #azFS1 mb < #azX mb run scoreboard players operation #azX mb = #azFS1 mb
execute if score #azF2 mb = #azNfF mb if score #azFS2 mb < #azX mb run scoreboard players set #azY mb 2
execute if score #azF2 mb = #azNfF mb if score #azFS2 mb < #azX mb run scoreboard players operation #azX mb = #azFS2 mb
execute if score #azF3 mb = #azNfF mb if score #azFS3 mb < #azX mb run scoreboard players set #azY mb 3
execute if score #azF3 mb = #azNfF mb if score #azFS3 mb < #azX mb run scoreboard players operation #azX mb = #azFS3 mb
execute if score #azF4 mb = #azNfF mb if score #azFS4 mb < #azX mb run scoreboard players set #azY mb 4
execute if score #azF4 mb = #azNfF mb if score #azFS4 mb < #azX mb run scoreboard players operation #azX mb = #azFS4 mb
execute if score #azF5 mb = #azNfF mb if score #azFS5 mb < #azX mb run scoreboard players set #azY mb 5
execute if score #azF5 mb = #azNfF mb if score #azFS5 mb < #azX mb run scoreboard players operation #azX mb = #azFS5 mb
execute if score #azF6 mb = #azNfF mb if score #azFS6 mb < #azX mb run scoreboard players set #azY mb 6
execute if score #azF6 mb = #azNfF mb if score #azFS6 mb < #azX mb run scoreboard players operation #azX mb = #azFS6 mb
execute if score #azF7 mb = #azNfF mb if score #azFS7 mb < #azX mb run scoreboard players set #azY mb 7
execute if score #azF7 mb = #azNfF mb if score #azFS7 mb < #azX mb run scoreboard players operation #azX mb = #azFS7 mb
execute if score #azY mb matches 0 run function rlk:mboss/azhdaha/fld/cancel_0
execute if score #azY mb matches 1 run function rlk:mboss/azhdaha/fld/cancel_1
execute if score #azY mb matches 2 run function rlk:mboss/azhdaha/fld/cancel_2
execute if score #azY mb matches 3 run function rlk:mboss/azhdaha/fld/cancel_3
execute if score #azY mb matches 4 run function rlk:mboss/azhdaha/fld/cancel_4
execute if score #azY mb matches 5 run function rlk:mboss/azhdaha/fld/cancel_5
execute if score #azY mb matches 6 run function rlk:mboss/azhdaha/fld/cancel_6
execute if score #azY mb matches 7 run function rlk:mboss/azhdaha/fld/cancel_7
