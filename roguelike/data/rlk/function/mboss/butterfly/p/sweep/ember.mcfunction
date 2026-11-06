# @s = a live trail segment hazard, at its floor point + 0.05, its yaw. The strike comes mbHzW - mbHzT - 1 ticks
# from now (the resume hook runs before this tick's hz/all); storage rlk:mboss bfr = the card's macro args.
scoreboard players operation #bfX mb = @s mbHzW
scoreboard players operation #bfX mb -= @s mbHzT
scoreboard players remove #bfX mb 1
execute if score #bfX mb matches ..0 run return 0
data modify storage rlk:mboss bfr set value {kind:"streak",pos:"~ ~ ~",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:2,s1:2,move:"0f,0f,0f",life:11,fade:3,col:14696512}
scoreboard players add #bfX mb 1
execute store result storage rlk:mboss bfr.life int 1 run scoreboard players get #bfX mb
function rlk:mboss/butterfly/fx/card with storage rlk:mboss bfr
