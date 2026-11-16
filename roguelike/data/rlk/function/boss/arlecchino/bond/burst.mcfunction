# 선혈의 충격 outside a window (@s = body): the crimson burst + true 2 % of the pool (clamped).
scoreboard players set #t3 kn 20
execute at @s positioned ~ ~1.4 ~ run function rlk:boss/arlecchino/fx/p/shock_hit
execute at @s run function rlk:boss/arlecchino/fx/snd/shock_hit
function rlk:boss/arlecchino/bond/true
