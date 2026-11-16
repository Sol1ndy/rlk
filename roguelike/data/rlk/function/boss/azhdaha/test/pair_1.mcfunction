# Force pair 1: legs hydro, tail cryo (recolours a live rig, badges, RES).
scoreboard players set #azLeg mb 2
scoreboard players set #azTail mb 4
data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:2,tail:4,i:1}
function rlk:boss/azhdaha/test/pair_sync
