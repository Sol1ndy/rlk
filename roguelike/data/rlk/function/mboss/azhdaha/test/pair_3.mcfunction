# Force pair 3: legs hydro, tail electro (recolours a live rig, badges, RES).
scoreboard players set #azLeg mb 2
scoreboard players set #azTail mb 3
data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:2,tail:3,i:3}
function rlk:mboss/azhdaha/test/pair_sync
