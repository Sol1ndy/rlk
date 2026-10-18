# Field opening (core service 20; clip warp_out, then warp_in_field at 34; @s = body): halo flip, warp-out
# at 13, violet glitch over the old spot, warp-in at the centre, unfold at 35, banner at 56.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound minecraft:block.chain.place hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
playsound minecraft:block.piston.extend hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
