# Append position spaces for an advance of 2 x #mmX (|#mmX| <= 1000).
scoreboard players operation #len mm = #mmX mm
scoreboard players operation #len mm += #mmX mm
execute if score #len mm matches 1.. run return run function rlk:minimap/offset_pos
scoreboard players operation #len mm *= #neg mm
function rlk:minimap/offset_neg
