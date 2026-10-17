# @s = body hovering 3 b up (rig): the 350 t timer, two stars from slots A/B, the cross sigil, haze, streams.
scoreboard players set #gdCP mb 3
scoreboard players set #gdTim mb 350
scoreboard players set #gdTimS mb 17
scoreboard players set #gdHaze mb 1
scoreboard players set #gdCsT mb 16
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/star/spawn_a
function rlk:mboss/guardian/star/spawn_b
function rlk:mboss/guardian/chaos/sigil
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 1 1.2 0.3
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 1 1.4 0.3
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.3
function rlk:mboss/guardian/hud/sub_chaos
