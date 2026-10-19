scoreboard players operation #azX mb = #azFE4 mb
scoreboard players operation #azX mb -= #azClk mb
execute if score #azX mb matches ..0 run return run function rlk:mboss/azhdaha/fld/cancel_4
data modify storage rlk:mboss az.nf set from storage rlk:mboss az.f4
execute store result storage rlk:mboss az.nf.life int 1 run scoreboard players get #azX mb
execute store result score #azNfF mb run data get storage rlk:mboss az.nf.fam
execute store result score #azNfA mb run data get storage rlk:mboss az.nf.area
execute if score #azF4 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA4 mb
execute if score #azF4 mb matches 1.. run scoreboard players remove #azFldN mb 1
scoreboard players set #azFG1 mb 0
scoreboard players set #azFG2 mb 0
scoreboard players set #azFG3 mb 0
function rlk:mboss/azhdaha/fld/remake_m with storage rlk:mboss az.f4
