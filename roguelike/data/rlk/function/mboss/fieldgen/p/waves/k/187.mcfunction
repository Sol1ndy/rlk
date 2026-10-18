# waves clock 187
function rlk:mboss/fieldgen/fx/p/wave_fire {r:9.1}
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^9.1 run function rlk:mboss/fieldgen/fx/snd/wave_ring
execute if score #fq21T mb matches 1 run function rlk:mboss/fieldgen/fx/p/wave_beam {h:4.1}
execute if score #fq21T mb matches 1 run function rlk:mboss/fieldgen/fx/snd/wave_beam
