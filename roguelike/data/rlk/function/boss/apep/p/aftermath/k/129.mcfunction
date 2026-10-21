# aftermath #apq32 129
execute if score #mbHitEv mb > #apq32H mb at @e[tag=rlk_body,limit=1] run function rlk:boss/apep/fx/snd/q2_tick
scoreboard players operation #apq32H mb = #mbHitEv mb
