# only start the dive when a straight dive onto the body's spot is open right now (else the fan may go; retry in 0.6 s)
execute unless function rlk:cm/rv/d_pre run scoreboard players set @s cmCd2 12
execute if score @s cmCd2 matches 1.. run return fail
function rlk:cm/rv/d_start
return 1
