# @s = target: true damage of $(pct) % of its max HP (mhpM / 100 x pct, overflow-safe). Colour = #mbTrueEl.
scoreboard players operation #mbTrue mb = @s mhpM
scoreboard players operation #mbTrue mb /= #c100 mb
$scoreboard players set #t mb $(pct)
scoreboard players operation #mbTrue mb *= #t mb
execute if score #mbTrue mb matches ..0 run scoreboard players set #mbTrue mb 1
function rlk:mboss/true_hit
