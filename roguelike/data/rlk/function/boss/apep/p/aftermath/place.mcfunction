# @s = body (B0): the three footprints (fix 10-22f): the player's distance band (3 b; #apq32P tenths) and a random
# layout of the band (12 each, aftermath.LAYOUTS: centres 7-17.4 b from the centre, 14-30 b apart,
# never near-equilateral, the nearest <= 9 b from the band's player), in the frame at the centre facing the player.
kill @e[tag=rlk_mb_ap_p32f]
scoreboard players set #apq32P mb 0
execute as @e[tag=rlk_body,limit=1] run function rlk:boss/apep/p/aftermath/pdist
execute store result score #apq32L mb run random value 0..11
execute if score #apq32P mb matches ..29 positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b0
execute if score #apq32P mb matches 30..59 positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b1
execute if score #apq32P mb matches 60..89 positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b2
execute if score #apq32P mb matches 90..119 positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b3
execute if score #apq32P mb matches 120..149 positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b4
execute if score #apq32P mb matches 150..179 positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b5
execute if score #apq32P mb matches 180..209 positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b6
execute if score #apq32P mb matches 210..239 positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b7
execute if score #apq32P mb matches 240.. positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/lay/b8
