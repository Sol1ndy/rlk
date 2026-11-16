# @s = the hazard (callers may run this `as` it from anywhere): remove it and its bound displays.
scoreboard players operation #rdOwner rd = @s rdHId
execute at @s as @e[tag=rlk_rd_hvis,distance=..0.05] if score @s rdVId = #rdOwner rd run kill @s
kill @s
