# @s = boss: may the groggy start now? (the module knows its scripted / invulnerable / mechanic states)
execute if entity @s[tag=rlk_mb_body] run return run function rlk:mboss/d/bal_ok
execute if entity @s[tag=rlk_raiden] run return run function rlk:boss/raiden/bal_ok
return fail
