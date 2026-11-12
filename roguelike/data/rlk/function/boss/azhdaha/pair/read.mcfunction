# The rolled pair from cprep.azhdaha.pair (s2.md 4.4); LOCAL fallback while no prep ran (the mid-boss path of
# the tests before AZ-CM): roll here.
execute unless data storage rlk:mboss cprep.azhdaha.pair run execute store result score #azPair mb run random value 0..3
execute unless data storage rlk:mboss cprep.azhdaha.pair if score #azPair mb matches 0 run data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:1,tail:3,i:0}
execute unless data storage rlk:mboss cprep.azhdaha.pair if score #azPair mb matches 1 run data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:2,tail:4,i:1}
execute unless data storage rlk:mboss cprep.azhdaha.pair if score #azPair mb matches 2 run data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:1,tail:4,i:2}
execute unless data storage rlk:mboss cprep.azhdaha.pair if score #azPair mb matches 3 run data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:2,tail:3,i:3}
execute store result score #azLeg mb run data get storage rlk:mboss cprep.azhdaha.pair.leg
execute store result score #azTail mb run data get storage rlk:mboss cprep.azhdaha.pair.tail
data modify storage rlk:mboss az.pair set from storage rlk:mboss cprep.azhdaha.pair
