# waves clock 187
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:9.1}
execute unless score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^9.1 run function rlk:mboss/fieldgen/fx/snd/wave_ring
execute if score #fq21T mb matches 1 unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_beam {h:4.26}
execute if score #fq21T mb matches 1 unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/snd/wave_beam
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:9.1}
execute if score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^9.1 run function rlk:mboss/fieldgen/fx/snd/wave_ring
execute if score #fq21T mb matches 1 if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_beam {h:3.601}
execute if score #fq21T mb matches 1 if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/snd/wave_beam
