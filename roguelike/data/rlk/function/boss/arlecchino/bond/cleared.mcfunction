# Her bond is gone from the player (bol 0 by any heal; @s any): 선혈의 충격 armed (one at a time, kept until
# used or the fight ends), the badge on the boss bar.
scoreboard players set #bonded kn 0
scoreboard players set #given kn 0
scoreboard players set #dot_t kn 0
scoreboard players set #shock kn 1
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1 ~ run particle minecraft:enchanted_hit ~ ~ ~ 0.4 0.8 0.4 0.1 20 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.8 0.3 0 16 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.8 1.4 0.27
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.wither.ambient hostile @a[tag=player] ~ ~ ~ 0.25 1.8 0
function rlk:boss/arlecchino/hud/sub
