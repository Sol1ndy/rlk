# @s = body, every 4 t: the FLANK-near dwell ring (6 samples = 24 t) and the proxy record (40 t).
function rlk:mboss/azhdaha/ai/sample
scoreboard players add #azFsI mb 1
execute if score #azFsI mb matches 6.. run scoreboard players set #azFsI mb 0
execute if score #azFsI mb matches 0 run scoreboard players operation #azFs0 mb = #azFN mb
execute if score #azFsI mb matches 1 run scoreboard players operation #azFs1 mb = #azFN mb
execute if score #azFsI mb matches 2 run scoreboard players operation #azFs2 mb = #azFN mb
execute if score #azFsI mb matches 3 run scoreboard players operation #azFs3 mb = #azFN mb
execute if score #azFsI mb matches 4 run scoreboard players operation #azFs4 mb = #azFN mb
execute if score #azFsI mb matches 5 run scoreboard players operation #azFs5 mb = #azFN mb
scoreboard players set #azDwell mb 0
scoreboard players operation #azDwell mb += #azFs0 mb
scoreboard players operation #azDwell mb += #azFs1 mb
scoreboard players operation #azDwell mb += #azFs2 mb
scoreboard players operation #azDwell mb += #azFs3 mb
scoreboard players operation #azDwell mb += #azFs4 mb
scoreboard players operation #azDwell mb += #azFs5 mb
# a flank proxy hit in the last 40 t from |s| >= 3 (#azPxHit = mbPart of the last hit, #azPxGT its gametime)
scoreboard players set #azPxF mb 0
execute store result score #azX mb run time query gametime
scoreboard players operation #azX mb -= #azPxGT mb
execute if score #azPxHit mb matches 2 if score #azX mb matches ..40 if score #azAs mb matches 3000.. run scoreboard players set #azPxF mb 1
execute if score #azPxHit mb matches 3 if score #azX mb matches ..40 if score #azAs mb matches 3000.. run scoreboard players set #azPxF mb 1
execute if score #azPxHit mb matches 4 if score #azX mb matches ..40 if score #azAs mb matches 3000.. run scoreboard players set #azPxF mb 1
execute if score #azPxHit mb matches 9 if score #azX mb matches ..40 if score #azAs mb matches 3000.. run scoreboard players set #azPxF mb 1
execute if score #azPxHit mb matches 10 if score #azX mb matches ..40 if score #azAs mb matches 3000.. run scoreboard players set #azPxF mb 1
execute if score #azPxHit mb matches 11 if score #azX mb matches ..40 if score #azAs mb matches 3000.. run scoreboard players set #azPxF mb 1
execute if score #azPxHit mb matches 12 if score #azX mb matches ..40 if score #azAs mb matches 3000.. run scoreboard players set #azPxF mb 1
