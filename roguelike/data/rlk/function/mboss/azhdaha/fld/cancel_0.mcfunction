# Field slot 0 ends now (cap, death, cleanup): the hazard, the kit card, the table.
kill @e[type=minecraft:marker,tag=rlk_mb_az_fld0]
function rlk:mboss/azhdaha/fx/tele/field_end {id:0}
execute if score #azF0 mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA0 mb
execute if score #azF0 mb matches 1.. run scoreboard players remove #azFldN mb 1
scoreboard players set #azF0 mb 0
data remove storage rlk:mboss az.f0
