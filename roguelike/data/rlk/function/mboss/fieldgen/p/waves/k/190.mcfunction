# waves clock 190
execute unless score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:10.75}
execute unless score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^10.75 run function rlk:mboss/fieldgen/fx/snd/wave_ring
execute if score #fgWvK mb matches 2 run function rlk:mboss/fieldgen/fx/p/wave_fire {r:10.75}
execute if score #fgWvK mb matches 2 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^10.75 run function rlk:mboss/fieldgen/fx/snd/wave_ring
