# Field slot 3 ends now (cap, death, cleanup): the hazard, the kit card, the table.
kill @e[type=minecraft:marker,tag=rlk_mb_az_fld3]
function rlk:mboss/azhdaha/kstub/tele/field_end
execute if score #azF3 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA3 mb
execute if score #azF3 mb matches 1.. run scoreboard players remove #azFldN mb 1
scoreboard players set #azF3 mb 0
data remove storage rlk:mboss az.f3
