# The floor was reached: the transition is queued (#azTr 1, #azTrN = the phase); bg T is cancelled, the orbs ride
# high; a released pattern ends now (its harmless tail cancelled).
scoreboard players set #azTr mb 1
scoreboard players operation #azTrN mb = #azPh mb
function rlk:boss/azhdaha/bg/cancel_t
scoreboard players set #azOrbHigh mb 1
scoreboard players set #azHudQ mb 1
execute if score #azPat mb matches 1.. if score #azPRel mb matches 1 run function rlk:boss/azhdaha/p/cut
