# Strike (@s = a decal part of the striking lane): the amber bar goes, the fill flashes white.
execute if entity @s[tag=rlk_mb_gd_p2bar] run return run kill @s
execute if entity @s[tag=rlk_mb_gd_p2fill] run data merge entity @s {block_state:{id:"minecraft:white_stained_glass"}}
