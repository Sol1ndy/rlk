# Between patterns (no walking, plan A.2): face the player, then choose. A queued rear check keeps her facing.
execute unless score @s rdSgRearQ matches 1 at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute unless score @s rdSgRearQ matches 1 at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdCool matches ..0 at @s run function rlk:boss/raiden/choose
