# 만겁: inside the dome (r, no pad) takes the hazard damage; anywhere else is fatal. Jumping does not help.
execute if score #rdR2 rd <= @s rdHE run return run function rlk:boss/raiden/hazard/land
scoreboard players add @s rdHHit 1
execute as @a[tag=player,scores={dead=0},limit=1] run function rlk:boss/raiden/hazard/fatal
