# (FIX STATE-1) A decision point inside a transition with an empty main slot (a step was lost, e.g. a service
# cancelled by /reload): the step of #azTr again (2 the leg special host, 3 the landslide, 4 the absorb, 5 the B3).
execute if score #azTr mb matches 2 run return run function rlk:mboss/azhdaha/tr/begin2
scoreboard players set #azPNew mb 1
scoreboard players set #azReqT mb 0
execute if score #azTr mb matches 3 run return run scoreboard players set #azPat mb 20
execute if score #azTr mb matches 4 if score #azTrN mb matches 1 run return run scoreboard players set #azPat mb 21
execute if score #azTr mb matches 4 run return run scoreboard players set #azPat mb 22
execute if score #azTr mb matches 5 run return run scoreboard players set #azPat mb 23
scoreboard players set #azPNew mb 0
function rlk:mboss/azhdaha/tr/done
