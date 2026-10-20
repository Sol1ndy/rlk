# Field slot 5 ends now (cap, death, cleanup): the hazard, the kit card, the table.
kill @e[type=minecraft:marker,tag=rlk_mb_az_fld5]
function rlk:mboss/azhdaha/kstub/tele/field_end
execute if score #azF5 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA5 mb
execute if score #azF5 mb matches 1.. run scoreboard players remove #azFldN mb 1
scoreboard players set #azF5 mb 0
data remove storage rlk:mboss az.f5
