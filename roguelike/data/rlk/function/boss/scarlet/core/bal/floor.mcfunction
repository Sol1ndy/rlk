# hr_design §1.3: CS1 / lead5 starts with a break pending (@s = body): the pending break is dropped and she keeps
# 3 pips (she is not broken inside a cutscene and does not come out of it full).
tag @s remove rlk_bal_pend
scoreboard players set @s bal 3
scoreboard players operation @s balT = #rd3 bal
scoreboard players set @s balF 0
function rlk:bal/ui/draw
