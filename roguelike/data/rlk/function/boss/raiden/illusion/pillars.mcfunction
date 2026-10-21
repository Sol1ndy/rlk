# As the boss: four spots on a ring of radius 13 about the arena centre, 90 deg apart, 45 deg off the bearing of
# the player from the centre; sky pillars there.
kill @e[tag=rlk_rd_ilspot]
execute at @e[tag=rlk_raiden_arena,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~45 0 run function rlk:boss/raiden/illusion/spots
execute as @e[tag=rlk_rd_ilspot] at @s run function rlk:boss/raiden/fx/bolt
