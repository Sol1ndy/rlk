# test 50 (@s = body, at it)
scoreboard players set #auxHpPct mb 5
scoreboard players set #auxRes mb 10
scoreboard players set #auxResEl mb 1
scoreboard players set #auxResElV mb 50
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4 positioned ~ 201 ~ run function rlk:mboss/aux/spawn
tag @e[tag=rlk_mb_auxlast,limit=1] add rlk_mb_cproto_aux
