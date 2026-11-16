# A normal-attack hit landed while 선혈의 충격 is armed (#shk_hit, set by on_hit; @s = body): inside a break
# window the break (core/break), else the crimson burst; the shock is spent either way.
scoreboard players set #shk_hit kn 0
execute unless score #shock kn matches 1 run return 0
scoreboard players set #shock kn 0
execute if entity @s[tag=rlk_kn_win] run return run function rlk:boss/arlecchino/core/break
function rlk:boss/arlecchino/bond/burst
execute if score #mbSt mb matches 1 run function rlk:boss/arlecchino/hud/sub
