# One lateral dash (@s = body, facing the player): 4 b to her right at the hover
# height over 4 t; the floor spot below must pass mv/ok, else the other side, else none.
execute at @s rotated as @s rotated ~ 0 positioned ^-4 ^ ^ positioned ~ 201 ~ if function rlk:mboss/mv/ok at @s rotated as @s rotated ~ 0 positioned ^-4 ^ ^ run return run function rlk:mboss/mv/glide {t:4}
execute at @s rotated as @s rotated ~ 0 positioned ^4 ^ ^ positioned ~ 201 ~ if function rlk:mboss/mv/ok at @s rotated as @s rotated ~ 0 positioned ^4 ^ ^ run return run function rlk:mboss/mv/glide {t:4}
