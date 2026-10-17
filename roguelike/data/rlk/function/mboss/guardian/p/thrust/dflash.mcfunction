# Strike (@s = a decal part of the striking lane): the amber bar goes, the fill flashes white.
execute if entity @s[tag=rlk_mb_gd_p1bar] run return run kill @s
execute if entity @s[tag=rlk_mb_gd_p1fill] run data merge entity @s {block_state:{id:"minecraft:white_stained_glass"}}
