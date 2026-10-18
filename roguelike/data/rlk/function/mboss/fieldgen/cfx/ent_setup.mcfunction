# Core fx ent_setup (vanilla particles / sounds; @s = body unless noted).
# @s = body: the folded device on the floor, dust and a low mechanical hum.
execute at @s run particle minecraft:block{block_state:"minecraft:tuff"} ~ ~0.3 ~ 1.2 0.1 1.2 0 10 force @a[tag=player]
execute at @s run playsound minecraft:block.respawn_anchor.ambient hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.2
