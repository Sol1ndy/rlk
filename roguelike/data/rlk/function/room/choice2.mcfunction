$execute store result score #oarg tmp run data get storage rlk:room pool[$(i)]
$data remove storage rlk:room pool[$(i)]
execute store result storage rlk:room a.t int 1 run scoreboard players get #oarg tmp
function rlk:room/choice3 with storage rlk:room a
