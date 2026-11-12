# The destination marker in front of the player (toward her), then the blink (movement/blink_to clamps it).
kill @e[tag=rlk_rd_blink_dest]
execute if score @s rdPat matches 11 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to
execute if score @s rdPat matches 16 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^5 positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to
execute if score @s rdPat matches 19 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^10 positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to
execute unless score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_start
