# As one card: expire; start the main interpolation one tick after the spawn; then the fade.
execute unless score @s mbS = @s mbS run return run kill @s
execute if score #bfTcNow mb >= @s mbS run return run kill @s
execute if entity @s[tag=rlk_mb_bf_tcgo] if score #bfTcNow mb > @s mbT run function rlk:mboss/butterfly/tc/go
scoreboard players add #bfTcN mb 1
execute if entity @s[tag=rlk_mb_bf_tcfd] if score #bfTcNow mb >= @s mbId run function rlk:mboss/butterfly/tc/fade
