# Force pair 0: legs pyro, tail electro (recolours a live rig, badges, RES).
scoreboard players set #azLeg mb 1
scoreboard players set #azTail mb 3
data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:1,tail:3,i:0}
function rlk:boss/azhdaha/test/pair_sync
