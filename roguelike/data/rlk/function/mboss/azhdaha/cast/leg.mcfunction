# The leg special into the cast slot (s2.md 6): #azCastReq (the AI pick or a test) else the rolled leg element
# (31 orbs Hydro, 32 meteors Pyro); #azCT 0 = the roar_rear tick; its cast hook now.
execute if score #azCast mb matches 1.. run function rlk:mboss/azhdaha/cast/cancel
scoreboard players operation #azX mb = #azCastReq mb
scoreboard players set #azCastReq mb 0
execute unless score #azX mb matches 31..32 if score #azLeg mb matches 2 run scoreboard players set #azX mb 31
execute unless score #azX mb matches 31..32 if score #azLeg mb matches 1 run scoreboard players set #azX mb 32
scoreboard players operation #azCast mb = #azX mb
scoreboard players set #azCT mb 0
execute if score #azCast mb matches 31 run return run function rlk:mboss/azhdaha/p/orbs/cast
execute if score #azCast mb matches 32 run return run function rlk:mboss/azhdaha/p/meteor/cast
