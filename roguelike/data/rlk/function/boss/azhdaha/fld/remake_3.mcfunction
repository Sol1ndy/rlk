scoreboard players operation #azX mb = #azFE3 mb
scoreboard players operation #azX mb -= #azClk mb
execute if score #azX mb matches ..0 run return run function rlk:boss/azhdaha/fld/cancel_3
data modify storage rlk:mboss az.nf set from storage rlk:mboss az.f3
execute store result storage rlk:mboss az.nf.life int 1 run scoreboard players get #azX mb
execute store result score #azNfF mb run data get storage rlk:mboss az.nf.fam
execute store result score #azNfA mb run data get storage rlk:mboss az.nf.area
execute if score #azF3 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA3 mb
execute if score #azF3 mb matches 1.. run scoreboard players remove #azFldN mb 1
# (FIX STATE-15) the table keeps its sequence (oldest-first caps), start tick and base life (refresh cap)
scoreboard players operation #azRS mb = #azFS3 mb
scoreboard players operation #azRT mb = #azFT3 mb
scoreboard players operation #azRB mb = #azFB3 mb
function rlk:boss/azhdaha/fld/remake_m with storage rlk:mboss az.f3
scoreboard players operation #azFS3 mb = #azRS mb
scoreboard players operation #azFT3 mb = #azRT mb
scoreboard players operation #azFB3 mb = #azRB mb
