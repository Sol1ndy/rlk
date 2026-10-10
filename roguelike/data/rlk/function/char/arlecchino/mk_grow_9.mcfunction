scoreboard players operation #ty tmp = @s armY
scoreboard players add #ty tmp 113
scoreboard players operation #tz tmp = @s armZ
scoreboard players add #tz tmp 11
execute store result storage rlk:st arm.ty float 0.001 run scoreboard players get #ty tmp
execute store result storage rlk:st arm.tz float 0.001 run scoreboard players get #tz tmp
function rlk:char/arlecchino/mk_grow_9_m with storage rlk:st arm
