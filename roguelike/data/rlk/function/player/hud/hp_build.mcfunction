scoreboard players operation @s hpKey = #hpN tmp
execute store result storage rlk:hud hn int 1 run scoreboard players get #hpN tmp
function rlk:player/hud/hp_set with storage rlk:hud
