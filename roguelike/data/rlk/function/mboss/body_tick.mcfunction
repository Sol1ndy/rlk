# @s = body, at @s. #mbT = clock of the current state (0 intro, 1 fight, 2 dying).
data merge entity @s {Motion:[0d,0d,0d],Fire:-1s}
scoreboard players add #mbT mb 1
execute if score #mbSt mb matches 0 run return run function rlk:mboss/intro_shell
execute if score #mbSt mb matches 1 run return run function rlk:mboss/fight_tick
execute if score #mbSt mb matches 2 run function rlk:mboss/death_shell
