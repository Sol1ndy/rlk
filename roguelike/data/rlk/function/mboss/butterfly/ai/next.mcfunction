# Next action. Test request > test lock (#mbLock 1-4 human pattern only, 11-14 butterfly pattern only (after
# a transformation), 15/16 form cycle only) > the form's rotation: human -> transformation when its stretch
# is over (first: 600 t of fight or 5 patterns, after a groggy 4 patterns); butterfly -> 달빛 해제
# after 4-5 patterns or 900 t. Only here, at a pattern boundary.
execute if score #bfPat mb matches 1.. run return 0
execute unless score #bfMv mb matches 0 run function rlk:mboss/butterfly/ai/mv0
execute if score #bfReq mb matches 1.. run return run function rlk:mboss/butterfly/ai/req
execute if score #mbLock mb matches 1..4 run return run function rlk:mboss/butterfly/ai/lock_h
execute if score #mbLock mb matches 11..14 run return run function rlk:mboss/butterfly/ai/lock_b
execute if score #mbLock mb matches 15..16 run return run function rlk:mboss/butterfly/ai/lock_cycle
execute if score #bfForm mb matches 2 run return run function rlk:mboss/butterfly/ai/next_b
function rlk:mboss/butterfly/ai/next_h
