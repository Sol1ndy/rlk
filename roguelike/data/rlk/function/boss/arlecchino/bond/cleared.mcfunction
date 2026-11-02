# Her bond is gone from the player (bol 0 by any heal; @s any): 선혈의 충격 armed (one at a time, kept until
# used or the fight ends), the badge on the boss bar.
scoreboard players set #bonded kn 0
scoreboard players set #given kn 0
scoreboard players set #dot_t kn 0
scoreboard players set #shock kn 1
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/shock_gain
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/arlecchino/fx/snd/shock_gain
function rlk:boss/arlecchino/hud/sub
