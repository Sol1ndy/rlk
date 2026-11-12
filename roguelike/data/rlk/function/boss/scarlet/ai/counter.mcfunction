# The counter trigger (core/fp: 4 player hits in 40 t while she recovers / idles): 70 %: A1 when the
# player is beside / behind her (|bearing| > 45 deg), A2 in front; their cooldowns and no-repeat kept. F1 (HR-26):
# only inside the near band (4.5 b): ranged hits from farther leave the decision to the far rule / band pick.
scoreboard players set #ctr hr 0
execute store result score #t hr run random value 1..100
execute if score #t hr matches 71.. run return fail
function rlk:boss/scarlet/ai/sample
execute unless score #ai_d2 hr matches ..202500 run return fail
scoreboard players set #t hr 0
execute if function rlk:boss/scarlet/ai/front run scoreboard players set #t hr 1
execute if score #t hr matches 1 if function rlk:boss/scarlet/ai/counter_a2 run return 1
execute if score #t hr matches 0 if function rlk:boss/scarlet/ai/counter_a1 run return 1
return fail
