execute store result score #c2t tmp run random value 0..1
execute if score #c2t tmp matches 0 run return run function rlk:cm/pc/sl_start
function rlk:cm/pc/sp_start
