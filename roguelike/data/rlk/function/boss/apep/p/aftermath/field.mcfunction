# At t40: the boss lands at the centre: a field ring pulse r 3 -> 26.0 (the field itself lies since B0) and the
# blast mask of the cast's safe group (800 per mille, t156-175, lethal unless this is the
# first cast: #apAft1 0).
execute positioned 440 201 8 run function rlk:boss/apep/fx/p/field_ring {r0:30,r1:260,dur:18}
execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/q2_release
execute if score #apAft1 mb matches 0 positioned 440 201 8 run function rlk:boss/apep/p/aftermath/hz_blast0
execute unless score #apAft1 mb matches 0 positioned 440 201 8 run function rlk:boss/apep/p/aftermath/hz_blast1
