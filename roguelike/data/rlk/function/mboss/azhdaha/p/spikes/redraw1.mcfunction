scoreboard players set #aq4R mb 51
scoreboard players operation #aq4R mb -= #azPT mb
data modify storage rlk:mboss az.tl set value {r:16,tell:14,nd:0,hold:3}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq4R mb
function rlk:mboss/azhdaha/fx/tele/disc_o with storage rlk:mboss az.tl
