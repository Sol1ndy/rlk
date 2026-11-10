# cs0: advance the shown tick to #t, key by key.
scoreboard players add #cavP cine 1
function rlk:char/cine/c/cs0/keys
execute if score #cavP cine < #t cine run function rlk:char/cine/c/cs0/catch
