# aftermath #apq32 134
function rlk:boss/apep/p/aftermath/heal
execute if score #mbHitEv mb > #apq32H mb at @e[tag=rlk_body,limit=1] run function rlk:boss/apep/fx/snd/q2_tick
scoreboard players operation #apq32H mb = #mbHitEv mb
execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/q2_rain
execute positioned 440 201 8 run function rlk:boss/apep/fx/p/beam_rain
