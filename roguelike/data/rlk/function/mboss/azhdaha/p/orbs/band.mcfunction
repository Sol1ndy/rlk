# @s = an orb marker, at it: #aq31H 0 normal band, 1 rides high (transitions / cine, the head-lane eye: front +-30 deg
# about the facing and < 11 b from the anchor, over a 42 safe circle), 2 harmless (growing / fading).
scoreboard players set #aq31H mb 0
execute if score #azOrbHigh mb matches 1 run scoreboard players set #aq31H mb 1
execute if score #aq31H mb matches 0 if entity @e[type=minecraft:husk,tag=rlk_mb_body,distance=..11,limit=1] run function rlk:mboss/azhdaha/p/orbs/eye
execute if score #aq31H mb matches 0 if entity @e[type=minecraft:marker,tag=rlk_mb_hzsafe,distance=..4.8] run scoreboard players set #aq31H mb 1
execute unless score #azBgLT mb matches 10.. run scoreboard players set #aq31H mb 2
execute if score #azBgLT mb >= #aq31E mb run scoreboard players set #aq31H mb 2
scoreboard players operation #aq31X mb = @s azF
execute as @e[type=minecraft:marker,tag=rlk_mb_az_orbhz] if score @s mbHzI = #aq31X mb run function rlk:mboss/azhdaha/p/orbs/hzb
