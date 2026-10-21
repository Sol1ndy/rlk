# A decision point with a queued transition: the message, then transition 1 = 20 -> 21, transition 2 = the leg
# special first (service 30) -> 20 -> 22 -> 23.
function rlk:mboss/azhdaha/tr/msg
execute if score #azTrN mb matches 2 run return run function rlk:mboss/azhdaha/tr/begin2
scoreboard players set #azTr mb 3
scoreboard players set #azPat mb 20
scoreboard players set #azPNew mb 1
scoreboard players set #azReqT mb 0
