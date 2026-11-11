# FN-cam: {x,y,z} = rlk:mboss camret (hundredths, rounded down). Written as offsets from the origin: an absolute x / z
# without a decimal point would be block-centred by the game (+0.5); 0.02 b up so the rounding never ends inside the floor.
$execute in minecraft:overworld positioned 0.0 0.02 0.0 run tp @s ~$(x) ~$(y) ~$(z)
