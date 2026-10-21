scoreboard players operation #azX mb = #azFE7 mb
scoreboard players operation #azX mb -= #azClk mb
execute if score #azX mb matches ..0 run return run function rlk:mboss/azhdaha/fld/cancel_7
data modify storage rlk:mboss az.nf set from storage rlk:mboss az.f7
execute store result storage rlk:mboss az.nf.life int 1 run scoreboard players get #azX mb
execute store result score #azNfF mb run data get storage rlk:mboss az.nf.fam
execute store result score #azNfA mb run data get storage rlk:mboss az.nf.area
execute if score #azF7 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA7 mb
execute if score #azF7 mb matches 1.. run scoreboard players remove #azFldN mb 1
# (FIX STATE-15) the table keeps its sequence (oldest-first caps), start tick and base life (refresh cap)
scoreboard players operation #azRS mb = #azFS7 mb
scoreboard players operation #azRT mb = #azFT7 mb
scoreboard players operation #azRB mb = #azFB7 mb
function rlk:mboss/azhdaha/fld/remake_m with storage rlk:mboss az.f7
scoreboard players operation #azFS7 mb = #azRS mb
scoreboard players operation #azFT7 mb = #azRT mb
scoreboard players operation #azFB7 mb = #azRB mb
