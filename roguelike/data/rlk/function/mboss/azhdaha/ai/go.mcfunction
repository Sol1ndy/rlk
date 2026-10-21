# Into the main slot (#azPick): the phase-3 replacements, repeat count, anti-stall count, the cast host for a leg
# special, the "first" lines; p/run starts it this tick (pattern clock 0 = clip tick 0 after any lead).
execute if score #azPick mb matches 5 if score #azPh mb matches 3..3 if score #azPaw mb matches 1..2 run scoreboard players set #azPick mb 10
execute if score #azPick mb matches 4 if score #azPh mb matches 3..3 if score #azTail mb matches 4 run scoreboard players set #azPick mb 45
execute if score #azPick mb matches 4 if score #azPh mb matches 3..3 if score #azTail mb matches 3 run scoreboard players set #azPick mb 46
# the repeat count (P5 at most 2 in a row) and the anti-stall count (TAIL-lane decisions without a tail pattern)
execute if score #azPick mb = #azLast mb run scoreboard players add #azRepN mb 1
execute unless score #azPick mb = #azLast mb run scoreboard players set #azRepN mb 1
execute if score #azPick mb matches 1..26 run scoreboard players operation #azLast mb = #azPick mb
execute if score #azPick mb matches 31..49 run scoreboard players operation #azLast mb = #azPick mb
execute unless score #azZone mb matches 6 run scoreboard players set #azTailN mb 0
execute if score #azZone mb matches 6 if score #azPick mb matches 1..26 unless score #azPick mb matches 7 unless score #azPick mb matches 8 run scoreboard players add #azTailN mb 1
execute if score #azPick mb matches 7 run scoreboard players set #azTailN mb 0
execute if score #azPick mb matches 8 run scoreboard players set #azTailN mb 0
# a leg special runs in the cast slot behind the core's cast host (service 30)
execute if score #azPick mb matches 31..32 run scoreboard players operation #azCastReq mb = #azPick mb
execute if score #azPick mb matches 31..32 run scoreboard players set #azPick mb 30
function rlk:mboss/azhdaha/ai/lines
scoreboard players operation #azPat mb = #azPick mb
scoreboard players set #azPNew mb 1
scoreboard players set #azReqT mb 0
