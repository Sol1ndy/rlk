# GENERATED (a table over the enabled entries, like the hook dispatchers of this folder): the warning glint
# (player/def/fx/glint) at the running boss's glint point. @s = the body husk, at it,
# rotated ~ 0. The point is the registry field "glint" [up, forward] in blocks from the body anchor (the chest / head of the
# visible rig at rest; mboss_lib.glint_of: default = 3/4 of the husk height for a husk-sized rig, 2 b for a px rig).
execute if score #mbId mb matches 1 positioned ^ ^2.8 ^0 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 2 positioned ^ ^3.2 ^0.2 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 3 positioned ^ ^4.4 ^0 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 99 positioned ^ ^2.05 ^0 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 98 positioned ^ ^2 ^0 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 10 positioned ^ ^2.6 ^3.2 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 11 positioned ^ ^3.3 ^1 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 20 positioned ^ ^1.75 ^0 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 97 positioned ^ ^1.83 ^0 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 12 positioned ^ ^2 ^0 run return run function rlk:player/def/fx/glint
execute if score #mbId mb matches 21 positioned ^ ^1.46 ^0 run return run function rlk:player/def/fx/glint
# (no running registry boss: 2 b over the body)
execute positioned ~ ~2 ~ run function rlk:player/def/fx/glint
