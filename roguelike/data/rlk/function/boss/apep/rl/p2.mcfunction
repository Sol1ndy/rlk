# /reload in phase 2: the stage (revival) re-makes the Heart, clears the walls, respawns the wave; parked again;
# the kit re-makes its dressing pool (the cards died with every rlk_mb_aux; ap_fx_api 0.12) at the arena centre.
function rlk:boss/apep/p/reload_d
function rlk:boss/apep/svc/park
function rlk:boss/apep/rev/reload
function rlk:boss/apep/arena/props_now
execute in minecraft:overworld positioned 440 201 8 run function rlk:boss/apep/fx/dress/redraw
scoreboard players set #apHudQ mb 1
