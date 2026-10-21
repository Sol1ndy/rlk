# At t40: the field release (the kit wash fills to t80 and holds to t176; the field ring
# r 3 -> 26.0) and the two mask hazards of the cast's safe group at the centre: the field ticks
# (30 per mille, never lethal, re-armed every 15 t, t80-154) and the blast
# (800 per mille, t156-175, lethal unless this is the first cast: #apAft1 0).
execute positioned 440 201 8 run function rlk:boss/apep/fx/tele/mask_wash {r:260,tell:40,hold:96}
execute positioned 440 201 8 run function rlk:boss/apep/fx/p/field_ring {r0:30,r1:260,dur:18}
execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/q2_release
execute positioned 440 201 8 run function rlk:boss/apep/p/aftermath/hz_ticks
execute if score #apAft1 mb matches 0 positioned 440 201 8 run function rlk:boss/apep/p/aftermath/hz_blast0
execute unless score #apAft1 mb matches 0 positioned 440 201 8 run function rlk:boss/apep/p/aftermath/hz_blast1
