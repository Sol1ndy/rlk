# No line of sight at 27 (or the destination blocked at 32): the cage shatters at the player (red/black
# shards, glass), the screen clears, no pull; #gp4Ok 2 = the swings still follow, in place (the pattern
# resolves instead of vanishing).
scoreboard players set #gp4Ok mb 2
execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~1 ~ 0.4 0.8 0.4 0 20 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~1.2 ~ 0.5 0.8 0.5 0 14 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.72f,0.18f,0.23f],scale:1.4} ~ ~1 ~ 0.5 0.9 0.5 0 12 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.9 0.6 0.3
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.chain.break hostile @a[tag=player] ~ ~ ~ 0.7 0.7 0.23
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 0.6 0.5 0.2
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p4cage]
function rlk:mboss/guardian/p/pull/scr_end
