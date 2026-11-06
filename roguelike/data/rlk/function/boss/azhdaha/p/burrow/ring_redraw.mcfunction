# @s = a live ring hazard: the outline again for its remaining tell
scoreboard players operation #t mb = @s mbHzW
scoreboard players operation #t mb -= @s mbHzT
execute if score #t mb matches ..0 run return 0
data modify storage rlk:mboss az.tl set value {r:34,el:5,nd:0,hold:3}
execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #t mb
function rlk:boss/azhdaha/fx/tele/chev_o with storage rlk:mboss az.tl
