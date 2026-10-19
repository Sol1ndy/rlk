# The nearest exit not tried yet (#pU1 side, #pU2 front end, #pU3 back end); #pEx = 1 left 2 right 3 front 4 back when
# its end point (the edge + 0.3 b) is clear of live disc / ring / line hazards.
scoreboard players set #pBest mb 0
scoreboard players set #pBd mb 2147483647
execute if score #pU1 mb matches 0 if score #pdS mb < #pBd mb run scoreboard players set #pBest mb 1
execute if score #pBest mb matches 1 run scoreboard players operation #pBd mb = #pdS mb
execute if score #pU2 mb matches 0 if score #pdF mb < #pBd mb run scoreboard players set #pBest mb 2
execute if score #pBest mb matches 2 run scoreboard players operation #pBd mb = #pdF mb
execute if score #pU3 mb matches 0 if score #pdB mb < #pBd mb run scoreboard players set #pBest mb 3
execute if score #pBest mb matches 3 run scoreboard players operation #pBd mb = #pdB mb
execute if score #pBest mb matches 0 run return 0
execute if score #pBest mb matches 1 run scoreboard players set #pU1 mb 1
execute if score #pBest mb matches 2 run scoreboard players set #pU2 mb 1
execute if score #pBest mb matches 3 run scoreboard players set #pU3 mb 1
# unit direction x1000 in the world (#fx #fz = the anchor forward from mv/local; left = (fz, -fx))
execute if score #pBest mb matches 1 if score #mbLs mb matches 0.. run function rlk:mboss/push/dir_left
execute if score #pBest mb matches 1 if score #mbLs mb matches ..-1 run function rlk:mboss/push/dir_right
execute if score #pBest mb matches 2 run function rlk:mboss/push/dir_front
execute if score #pBest mb matches 3 run function rlk:mboss/push/dir_back
scoreboard players operation #pDist mb = #pBd mb
scoreboard players add #pDist mb 300
scoreboard players operation #peX mb = #pux mb
scoreboard players operation #peX mb *= #pDist mb
scoreboard players operation #peX mb /= #c1000 mb
scoreboard players operation #peX mb += #pbx mb
scoreboard players operation #peZ mb = #puz mb
scoreboard players operation #peZ mb *= #pDist mb
scoreboard players operation #peZ mb /= #c1000 mb
scoreboard players operation #peZ mb += #pbz mb
function rlk:mboss/push/end_ok
execute if score #pOK mb matches 1 run scoreboard players operation #pEx mb = #pDir mb
