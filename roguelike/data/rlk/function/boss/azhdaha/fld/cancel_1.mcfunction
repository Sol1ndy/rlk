# Field slot 1 ends now (cap, death, cleanup): the hazard, the kit card, the table.
kill @e[type=minecraft:marker,tag=rlk_mb_az_fld1]
function rlk:boss/azhdaha/fx/tele/field_end {id:1}
execute if score #azF1 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA1 mb
execute if score #azF1 mb matches 1.. run scoreboard players remove #azFldN mb 1
scoreboard players set #azF1 mb 0
data remove storage rlk:mboss az.f1
