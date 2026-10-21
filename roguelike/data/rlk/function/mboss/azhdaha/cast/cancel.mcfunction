# The cast slot stops now (selectors only in the special's cancel).
execute if score #azCast mb matches 31 run function rlk:mboss/azhdaha/p/orbs/cancel
execute if score #azCast mb matches 32 run function rlk:mboss/azhdaha/p/meteor/cancel
scoreboard players set #azCast mb 0
