# The rest px set of the form and stance (phase 1 p1; phase 3 p3u UPRIGHT / p3c CROUCH).
execute if score #apPh mb matches ..1 run return run function rlk:mboss/apep/px/p1
execute if score #apPh mb matches 3 if score #apStance mb matches 1 run return run function rlk:mboss/apep/px/p3u
execute if score #apPh mb matches 3 run return run function rlk:mboss/apep/px/p3c
