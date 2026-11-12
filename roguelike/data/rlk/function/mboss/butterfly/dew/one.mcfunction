# #bfX = angle (deg); a random radius.
execute store result storage rlk:mboss bfd.a double 1 run scoreboard players get #bfX mb
execute store result score #bfY mb run random value 60..140
execute store result storage rlk:mboss bfd.r double 0.1 run scoreboard players get #bfY mb
function rlk:mboss/butterfly/dew/at with storage rlk:mboss bfd
