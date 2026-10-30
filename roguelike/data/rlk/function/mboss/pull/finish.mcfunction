scoreboard players set #pkbBlocked tmp 0
function rlk:player/knockback/check
execute if score #pkbBlocked tmp matches 0 run tp @e[tag=rlk_body,limit=1] ~ ~ ~
execute if score @s mbPlF matches 1 if entity @e[tag=rlk_mb_body,limit=1] as @a[tag=player,limit=1] run rotate @s facing entity @e[tag=rlk_mb_body,limit=1] eyes
kill @s
