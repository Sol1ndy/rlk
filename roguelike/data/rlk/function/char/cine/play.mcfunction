# function rlk:char/cine/play {clip:"cs0"|"cs1"|"repel"|"ending"|"coda"}: selects the clip; #cavT is the module's.
scoreboard objectives add cine dummy
$function rlk:char/cine/c/$(clip)/sel
