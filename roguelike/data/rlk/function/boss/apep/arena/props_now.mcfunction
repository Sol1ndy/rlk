# The props of the current look (reload): look_ap_oasis (cm.md 3.3), else the phase.
execute if data storage rlk:mboss {look_ap_oasis:"lush"} run return run function rlk:boss/apep/arena/props_lush
execute if score #apPh mb matches 3 run return run function rlk:boss/apep/arena/props_lush
function rlk:boss/apep/arena/props_withered
