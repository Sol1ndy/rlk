# waves clock 176
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_burst
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/snd/wave_burst
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_burst
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/snd/wave_burst
