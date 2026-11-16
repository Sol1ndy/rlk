# waves clock 177
execute if score #fq21T mb matches 1 unless score #fgWvK mb matches 2 positioned ~ ~4.24 ~ run function rlk:mboss/fieldgen/fx/p/wave_pulse
execute if score #fq21T mb matches 1 if score #fgWvK mb matches 2 positioned ~ ~2.45 ~ run function rlk:mboss/fieldgen/fx/p/wave_pulse
execute if score #fq21T mb matches 1 run function rlk:mboss/fieldgen/p/waves/mkx
