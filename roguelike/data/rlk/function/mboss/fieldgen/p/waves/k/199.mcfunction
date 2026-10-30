# waves clock 199
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:15.7}
execute unless score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^15.7 run function rlk:mboss/fieldgen/fx/snd/wave_ring
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:15.7}
execute if score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^15.7 run function rlk:mboss/fieldgen/fx/snd/wave_ring
