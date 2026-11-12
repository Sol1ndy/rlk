# @s = a pending keep hazard (rlk_mb_ap_p31k): its decal again (r 4.2) with the ticks left to its strike.
scoreboard players operation #apq31X mb = @s mbHzW
scoreboard players operation #apq31X mb -= @s mbHzT
execute if score #apq31X mb matches ..0 run return 0
data modify storage rlk:mboss ap.p31d set value {r:42,el:7,nd:0,hold:3,tell:1}
execute store result storage rlk:mboss ap.p31d.tell int 1 run scoreboard players get #apq31X mb
function rlk:boss/apep/fx/tele/disc_o with storage rlk:mboss ap.p31d
