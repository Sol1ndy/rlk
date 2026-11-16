# B2 hop (@s = body): 3 b sideways over 12 t (mv/leap, apex 0.6 b), a random side first; the spot must pass mv/ok.
execute store result score #b2_s tk run random value 0..1
execute if score #b2_s tk matches 0 at @s rotated as @s rotated ~ 0 positioned ^3 ^ ^ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:12,h:6}
execute at @s rotated as @s rotated ~ 0 positioned ^-3 ^ ^ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:12,h:6}
execute at @s rotated as @s rotated ~ 0 positioned ^3 ^ ^ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:12,h:6}
