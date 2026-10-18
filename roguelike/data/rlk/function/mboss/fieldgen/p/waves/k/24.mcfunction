# waves clock 24
function rlk:mboss/fieldgen/fx/p/wave_beam {h:4.1}
function rlk:mboss/fieldgen/fx/snd/wave_beam
function rlk:mboss/fieldgen/fx/p/wave_fire {r:2.5}
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^2.5 run function rlk:mboss/fieldgen/fx/snd/wave_ring
