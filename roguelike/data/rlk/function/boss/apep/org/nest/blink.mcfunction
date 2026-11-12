# The blink: out 0-2, moved at 3 to 5 b from the player (on the player -> 둥지 line, inside the walk
# disc, off the cradle), in 3-6.
execute if score @s apT matches 3 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^5 run tp @s ~ 201 ~
execute if score @s apT matches 3 run function rlk:mboss/ar/clampw
execute if score @s apT matches 3 run function rlk:boss/apep/org/nest/push_out
execute if score @s apT matches 3 at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
execute if score @s apT matches 3 run function rlk:boss/apep/om/face
execute if score @s apT matches 3 at @s positioned ~ ~1.2 ~ run function rlk:boss/apep/fx/p/blink_flash
execute if score @s apT matches 6.. run scoreboard players set @s apS 1
