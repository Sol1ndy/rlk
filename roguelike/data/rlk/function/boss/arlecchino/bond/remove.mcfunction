# @s = the player: bol -= min(bol, #given); the value-change hooks only (no clear hooks).
execute unless score @s bol matches 1.. run return 0
scoreboard players operation #t kn = @s bol
execute if score #t kn > #given kn run scoreboard players operation #t kn = #given kn
execute if score #t kn matches ..0 run return 0
scoreboard players operation @s bol -= #t kn
function rlk:player/bol/on_change
