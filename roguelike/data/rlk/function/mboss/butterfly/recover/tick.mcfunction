scoreboard players add #bfT mb 1
execute if score #bfT mb matches 1..24 run function rlk:mboss/mv/turn {max:9}
execute if score #bfT mb matches 24 run function rlk:mboss/butterfly/rig_stub/play/chain_reform
# the crescent chain re-forms at her left side (display frame: ^+x = left)
execute if score #bfT mb matches 24 run execute rotated as @s rotated ~ 0 positioned ^0.5 ^1.5 ^0.1 run function rlk:mboss/butterfly/fx/p/chain_reform
execute if score #bfT mb matches 30 run function rlk:mboss/butterfly/fx/snd/chain_reform
execute if score #bfT mb matches 30 run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.1} ~ ~1.8 ~ 0.6 0.6 0.6 0 10 force @a[tag=player]
execute if score #bfT mb matches 42.. run function rlk:mboss/butterfly/groggy/end
