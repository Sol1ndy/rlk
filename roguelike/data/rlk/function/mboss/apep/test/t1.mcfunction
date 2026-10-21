# 20: T1 now (from phase 1; phase 2 / 3 first jump to phase 1).
execute unless score #apPh mb matches 1 run function rlk:mboss/apep/ph/ready_1
function rlk:mboss/apep/ph/cut
scoreboard players set #apReq mb 20
scoreboard players set #apCool mb 1
