# As the boss: four spots 13 b from the player, 90 deg apart, diagonal to her bearing; sky pillars there.
kill @e[tag=rlk_rd_ilspot]
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~45 0 positioned ~ 201 ~ run function rlk:boss/raiden/illusion/spots
execute as @e[tag=rlk_rd_ilspot] at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] facing entity @s feet rotated ~ 0 positioned ^ ^ ^20 run tp @s ~ ~ ~
execute as @e[tag=rlk_rd_ilspot] at @s run function rlk:boss/raiden/fx/bolt
