# Clicks on the proxies of cproto (interaction attack / interaction data) go through the normal click input, every
# live tick (the click shield path of combat/mshield_tick).
execute as 524c4b4d-4350-4400-8000-000000000041 if data entity @s attack at @s run function rlk:combat/input/poll_attack
execute as 524c4b4d-4350-4400-8000-000000000041 if data entity @s interaction at @s run function rlk:combat/input/poll_right
execute as 524c4b4d-4350-4400-8000-000000000042 if data entity @s attack at @s run function rlk:combat/input/poll_attack
execute as 524c4b4d-4350-4400-8000-000000000042 if data entity @s interaction at @s run function rlk:combat/input/poll_right
