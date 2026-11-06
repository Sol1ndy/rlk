# @s = body: one run tick (1.0 b/t while inside the arena), the disc rides the body; at the end
# the disc ends and charge_stop plays.
scoreboard players remove #aq9R mb 1
execute at @s positioned ^ ^ ^1.0 unless function rlk:mboss/mv/ok run scoreboard players set #aq9R mb 0
execute if score #aq9R mb matches 0.. at @s positioned ^ ^ ^1.0 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute at @s as @e[type=minecraft:marker,tag=rlk_mb_az_p9run] run tp @s ~ ~ ~
scoreboard players set #azNoPush mb 1
scoreboard players operation #azM mb = #azPT mb
scoreboard players operation #azM mb %= #azK4 mb
execute if score #azM mb matches 0 run function rlk:boss/azhdaha/fx/p/dust_trail
execute if score #azM mb matches 0 run function rlk:boss/azhdaha/fx/snd/charge_gallop
execute if score #aq9R mb matches ..0 run function rlk:boss/azhdaha/p/burrow/run_stop
