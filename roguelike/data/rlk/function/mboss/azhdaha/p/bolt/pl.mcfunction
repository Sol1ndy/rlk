# @s = the player circle (at the player's feet): moved 5 b toward the centre (when farther), kept <= 24 b.
execute if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=5..,limit=1] facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^5
function rlk:mboss/azhdaha/u/clamp_r {r:24}
