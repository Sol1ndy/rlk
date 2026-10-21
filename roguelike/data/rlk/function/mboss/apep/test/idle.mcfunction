# 99: idle (whatever runs is cut; the phase stays).
function rlk:mboss/apep/ph/cut
scoreboard players set #apCool mb 40
execute if score #apPh mb matches 1 run function rlk:mboss/apep/svc/px_rest
execute if score #apPh mb matches 3 run function rlk:mboss/apep/svc/px_rest
