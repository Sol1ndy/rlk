# Force pair 2: legs pyro, tail cryo (recolours a live rig, badges, RES).
scoreboard players set #azLeg mb 1
scoreboard players set #azTail mb 4
data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:1,tail:4,i:2}
function rlk:mboss/azhdaha/test/pair_sync
