# The kit's meter_hit as the body at the rig core: the field core 4.1 b, or where the closing
# wave_drop has it (down to the floor and back up: fix round FID-4).
execute if score #fgPat mb matches 21 if score #fgWvK mb matches 2 run return run function rlk:mboss/fieldgen/brk/hit_wd
execute positioned ~ ~4.1 ~ run function rlk:mboss/fieldgen/fx/hud/meter_hit
