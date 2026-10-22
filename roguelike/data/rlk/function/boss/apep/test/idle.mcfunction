# 99: idle (whatever runs is cut; the phase stays).
function rlk:boss/apep/ph/cut
scoreboard players set #apCool mb 40
execute if score #apPh mb matches 1 run function rlk:boss/apep/svc/px_rest
execute if score #apPh mb matches 3 run function rlk:boss/apep/svc/px_rest
