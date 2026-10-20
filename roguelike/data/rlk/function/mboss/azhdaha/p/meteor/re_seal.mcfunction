scoreboard players set #aq32X mb 55
scoreboard players operation #aq32X mb -= #azCT mb
data modify storage rlk:mboss az.tl set value {r:52,tell:1,el:1,hold:3}
execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq32X mb
function rlk:mboss/azhdaha/fx/tele/seal8 with storage rlk:mboss az.tl
