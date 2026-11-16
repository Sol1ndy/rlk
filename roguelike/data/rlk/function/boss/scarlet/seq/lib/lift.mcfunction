# @s = a camera stand on a low eye point of a staged shot, placed and aimed: the lens is not left inside a plant of
# the field (dry grass; crimson roots in the crimson look; 1 b tall): its own cell or the cell 0.9 b along its
# view holds one -> the stand goes to 1.15 b over the floor (the caller aims it again).
execute at @s if block ~ ~ ~ minecraft:short_dry_grass run return run execute at @s run tp @s ~ 202.15 ~
execute at @s if block ~ ~ ~ minecraft:tall_dry_grass run return run execute at @s run tp @s ~ 202.15 ~
execute at @s if block ~ ~ ~ minecraft:crimson_roots run return run execute at @s run tp @s ~ 202.15 ~
execute at @s rotated ~ 0 positioned ^ ^ ^0.9 if block ~ ~ ~ minecraft:short_dry_grass run return run execute at @s run tp @s ~ 202.15 ~
execute at @s rotated ~ 0 positioned ^ ^ ^0.9 if block ~ ~ ~ minecraft:tall_dry_grass run return run execute at @s run tp @s ~ 202.15 ~
execute at @s rotated ~ 0 positioned ^ ^ ^0.9 if block ~ ~ ~ minecraft:crimson_roots run return run execute at @s run tp @s ~ 202.15 ~
