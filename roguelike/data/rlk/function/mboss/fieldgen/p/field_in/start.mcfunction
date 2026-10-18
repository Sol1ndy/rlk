# Field opening (core service 20; clip warp_out, then warp_in_field at 34; @s = body): halo flip, warp-out
# at 13, violet glitch over the old spot, warp-in at the centre, unfold at 35, banner at 56.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute rotated as @s rotated ~ 0 positioned ^ ^6.1 ^ run function rlk:mboss/fieldgen/fx/p/halo_flip
function rlk:mboss/fieldgen/fx/snd/halo_flip
