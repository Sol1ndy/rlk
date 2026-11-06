# At the ring-A1 point, rotated along the velocity line: three rock points (+3 / +6 / +9 b)
function rlk:mboss/grp_new
scoreboard players operation #aq9GR mb = #mbGrp mb
execute positioned ^ ^ ^3.0 run function rlk:boss/azhdaha/p/burrow/rock_one
execute positioned ^ ^ ^6.0 run function rlk:boss/azhdaha/p/burrow/rock_one
execute positioned ^ ^ ^9.0 run function rlk:boss/azhdaha/p/burrow/rock_one
