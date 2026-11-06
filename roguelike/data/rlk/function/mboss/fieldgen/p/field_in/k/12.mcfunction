# field_in clock 12
execute positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/warp_out
function rlk:mboss/fieldgen/fx/snd/warp_out
execute if entity @a[tag=player,distance=..8] run function rlk:mboss/fieldgen/fx/hud/flash_white
