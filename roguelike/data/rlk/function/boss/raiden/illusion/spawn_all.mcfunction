# Base direction: diagonal to the player's bearing, so nobody runs straight at them.
execute if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_raiden_arena,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~45 0 run function rlk:boss/raiden/illusion/spawn_ring
execute unless entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_raiden_arena,limit=1] rotated 45 0 run function rlk:boss/raiden/illusion/spawn_ring
