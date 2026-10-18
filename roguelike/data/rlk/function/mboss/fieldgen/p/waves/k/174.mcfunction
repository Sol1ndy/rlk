# waves clock 174
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_band {r0:25,r1:212,w:25,dur:34}
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_beam {h:4.11}
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/snd/wave_beam
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_band {r0:25,r1:212,w:25,dur:34}
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_beam {h:3.6}
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/snd/wave_beam
