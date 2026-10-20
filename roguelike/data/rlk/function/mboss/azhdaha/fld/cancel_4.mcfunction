# Field slot 4 ends now (cap, death, cleanup): the hazard, the kit card, the table.
kill @e[type=minecraft:marker,tag=rlk_mb_az_fld4]
function rlk:mboss/azhdaha/fx/tele/field_end {id:4}
execute if score #azF4 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA4 mb
execute if score #azF4 mb matches 1.. run scoreboard players remove #azFldN mb 1
scoreboard players set #azF4 mb 0
data remove storage rlk:mboss az.f4
