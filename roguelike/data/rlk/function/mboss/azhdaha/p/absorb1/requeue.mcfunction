# The leg special as the next pick (#azReq 30 = the cast host; #azCastReq = the rolled leg element's).
execute if score #azLeg mb matches 2 run scoreboard players set #azCastReq mb 31
execute if score #azLeg mb matches 1 run scoreboard players set #azCastReq mb 32
scoreboard players set #azReq mb 30
