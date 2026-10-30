# Callable from anywhere (module intro hook, tests): the fight state starts, the body becomes targetable.
execute unless score #mbSt mb matches 0 run return 0
tag @e[tag=rlk_mb_body] remove rlk_mb_inv
scoreboard players set #mbSt mb 1
scoreboard players set #mbT mb 0
