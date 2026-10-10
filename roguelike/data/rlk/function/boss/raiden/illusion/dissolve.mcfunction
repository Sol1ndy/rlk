# As an illusion husk at its feet: it scatters like the boss does (boss = art owner).
execute rotated as @s as @e[tag=rlk_raiden,limit=1] run rotate @s ~ 0
execute as @e[tag=rlk_raiden,limit=1] run function rlk:boss/raiden/movement/depart
function rlk:boss/raiden/illusion/vanish
