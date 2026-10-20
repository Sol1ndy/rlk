# Field slot 6 ends now (cap, death, cleanup): the hazard, the kit card, the table.
kill @e[type=minecraft:marker,tag=rlk_mb_az_fld6]
function rlk:mboss/azhdaha/fx/tele/field_end {id:6}
execute if score #azF6 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA6 mb
execute if score #azF6 mb matches 1.. run scoreboard players remove #azFldN mb 1
scoreboard players set #azF6 mb 0
data remove storage rlk:mboss az.f6
