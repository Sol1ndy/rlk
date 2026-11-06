# Field slot 2 ends now (cap, death, cleanup): the hazard, the kit card, the table.
kill @e[type=minecraft:marker,tag=rlk_mb_az_fld2]
function rlk:boss/azhdaha/fx/tele/field_end {id:2}
execute if score #azF2 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA2 mb
execute if score #azF2 mb matches 1.. run scoreboard players remove #azFldN mb 1
scoreboard players set #azF2 mb 0
data remove storage rlk:mboss az.f2
