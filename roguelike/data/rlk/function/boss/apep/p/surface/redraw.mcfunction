# @s = a pending keep hazard (rlk_mb_ap_p36k): its decal again (r 3.6) with the ticks left to its strike.
scoreboard players operation #apq36X mb = @s mbHzW
scoreboard players operation #apq36X mb -= @s mbHzT
execute if score #apq36X mb matches ..0 run return 0
data modify storage rlk:mboss ap.p36d set value {r:36,el:7,nd:0,hold:3,tell:1}
execute store result storage rlk:mboss ap.p36d.tell int 1 run scoreboard players get #apq36X mb
function rlk:boss/apep/fx/tele/disc with storage rlk:mboss ap.p36d
