# waves clock 180
execute if score #fq21T mb matches 1 unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_band {r0:25,r1:212,w:25,dur:34}
execute if score #fq21T mb matches 1 if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_band {r0:25,r1:212,w:25,dur:34}
