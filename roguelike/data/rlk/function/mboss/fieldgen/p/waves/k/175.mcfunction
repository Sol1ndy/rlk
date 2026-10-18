# waves clock 175
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_beam {h:4.26}
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/snd/wave_beam
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:2.5}
execute unless score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^2.5 run function rlk:mboss/fieldgen/fx/snd/wave_ring
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_beam {h:3.601}
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/snd/wave_beam
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:2.5}
execute if score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^2.5 run function rlk:mboss/fieldgen/fx/snd/wave_ring
