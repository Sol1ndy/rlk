# The dive target (C / E; @s = body): the lock moved 1.5 b toward her (when it stays farther than 2.5 b from
# her and passes mv/ok), so she lands in front of the player, not on them; the impact is centred there.
execute as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] at @s unless entity @e[type=minecraft:husk,tag=rlk_mb_body,distance=..2.5] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.5 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
