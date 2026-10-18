# Core fx count (vanilla particles / sounds; @s = body unless noted).
# @s = body: a counted hit: a gold crack glint on the core bubble (about 3.8 b up), a quiet chime.
execute at @s run particle minecraft:crit ~ ~3.8 ~ 0.5 0.5 0.5 0.2 6 force @a[tag=player]
execute at @s run particle minecraft:dust{color:[0.992f,0.984f,0.82f],scale:1} ~ ~3.8 ~ 0.5 0.5 0.5 0 4 force @a[tag=player]
execute at @s run playsound minecraft:block.amethyst_block.hit hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:block.chain.hit hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
