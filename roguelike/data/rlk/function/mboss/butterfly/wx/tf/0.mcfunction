# S2 transformation fx, clock 0 (@s = body, at it; the core's p/transform calls it).
# t0 the green vertical glow sheath wraps her lower body (kit tf_sheath), the cocoon glow recipe.
execute rotated as @s rotated ~ 0 positioned ~ ~1.6 ~ run function rlk:mboss/butterfly/fx/p/tf_sheath
function rlk:mboss/butterfly/fx/snd/transform_glow
particle minecraft:dust{color:[0.71f,0.941f,0.537f],scale:1.3} ~ ~1.0 ~ 0.3 0.7 0.3 0 10 force @a[tag=player]
particle minecraft:dust{color:[0.314f,0.545f,0.565f],scale:0.8} ~ ~1.0 ~ 0.35 0.7 0.35 0 4 force @a[tag=player]
