# The total lingering area <= 220 b2: the oldest (of the family, else any) goes until it fits.
scoreboard players operation #azX mb = #azFldA mb
scoreboard players operation #azX mb += #azNfA mb
execute if score #azX mb matches ..220 run return 0
execute if score #azFldN mb matches 0 run return 0
function rlk:boss/azhdaha/fld/cancel_oldest_fam
scoreboard players operation #azX mb = #azFldA mb
scoreboard players operation #azX mb += #azNfA mb
execute if score #azX mb matches 221.. run function rlk:boss/azhdaha/fld/cancel_oldest
scoreboard players operation #azX mb = #azFldA mb
scoreboard players operation #azX mb += #azNfA mb
execute if score #azX mb matches 221.. if score #azFldN mb matches 1.. run function rlk:boss/azhdaha/fld/cap_area
