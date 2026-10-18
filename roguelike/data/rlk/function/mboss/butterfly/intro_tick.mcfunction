# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end). The entrance clip has
# its tick t at intro tick t + 1: cocoon over a glowing floor disc, nameplate chime (57), glow ramp
# (61), whiteout (71), burst into crystal shards (79), the drop, landing (90), she stands
# (106); the fight at intro 108. No damage.
function rlk:mboss/butterfly/rig_stub/tick
scoreboard players operation #bfM mb = #mbT mb
scoreboard players operation #bfM mb %= #bfK4 mb
execute if score #bfM mb matches 0 if score #mbT mb matches 1..79 run function rlk:mboss/butterfly/intro/hover
execute if score #mbT mb matches 58 run function rlk:mboss/butterfly/intro/name
execute if score #mbT mb matches 1 run execute positioned ~ ~2.0 ~ run function rlk:mboss/butterfly/fx/p/motes
execute if score #mbT mb matches 21 run execute positioned ~ ~2.0 ~ run function rlk:mboss/butterfly/fx/p/motes
execute if score #mbT mb matches 41 run execute positioned ~ ~2.0 ~ run function rlk:mboss/butterfly/fx/p/motes
execute if score #mbT mb matches 62 run function rlk:mboss/butterfly/intro/glow_snd
execute if score #bfM mb matches 0..1 if score #mbT mb matches 62..79 run function rlk:mboss/butterfly/intro/glow
execute if score #mbT mb matches 72 run function rlk:mboss/butterfly/intro/white
execute if score #mbT mb matches 80 run function rlk:mboss/butterfly/intro/burst
execute if score #bfM mb matches 0 if score #mbT mb matches 81..90 run function rlk:mboss/butterfly/intro/fall
execute if score #mbT mb matches 83 run function rlk:mboss/butterfly/fx/snd/cocoon_tail
execute if score #mbT mb matches 89 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.5 1.7 0.17
execute if score #mbT mb matches 91 run function rlk:mboss/butterfly/intro/land
execute if score #mbT mb matches 108..999 run function rlk:mboss/butterfly/intro/done
