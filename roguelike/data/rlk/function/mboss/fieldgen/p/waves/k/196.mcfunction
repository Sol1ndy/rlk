# waves clock 196
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:14.05}
execute unless score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^14.05 run function rlk:mboss/fieldgen/fx/snd/wave_ring
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:14.05}
execute if score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^14.05 run function rlk:mboss/fieldgen/fx/snd/wave_ring
