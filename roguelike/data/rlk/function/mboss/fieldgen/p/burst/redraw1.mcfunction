# @s = the blast hazard marker, at it. Ticks to the strike: mbHzW - mbHzT - 1 (the module tick runs before hz/all).
scoreboard players operation #fgX mb = @s mbHzW
scoreboard players operation #fgX mb -= @s mbHzT
scoreboard players remove #fgX mb 1
execute if score #fgX mb matches ..0 run return 0
execute store result storage rlk:mboss fg.rd5.tell int 1 run scoreboard players get #fgX mb
data modify storage rlk:mboss fg.rd5 merge value {r:120,el:6,hold:3}
execute rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/rim with storage rlk:mboss fg.rd5
# the dark disc: only once the timeline drew it (7); growth left = ticks left - 15, r0 = R - (R - 3.5) x left / 26
execute unless score #fgPT mb matches 8.. run return 0
scoreboard players operation #fq5G mb = #fgX mb
scoreboard players remove #fq5G mb 15
execute if score #fq5G mb matches ..0 run scoreboard players set #fq5G mb 0
scoreboard players operation #fq5R mb = #fq5G mb
scoreboard players set #fq5K mb 85
scoreboard players operation #fq5R mb *= #fq5K mb
scoreboard players set #fq5K mb 26
scoreboard players operation #fq5R mb /= #fq5K mb
scoreboard players set #fq5K mb 120
scoreboard players operation #fq5K mb -= #fq5R mb
execute store result storage rlk:mboss fg.rd5.r0 int 1 run scoreboard players get #fq5K mb
execute if score #fq5G mb matches ..0 run scoreboard players set #fq5G mb 1
execute store result storage rlk:mboss fg.rd5.grow int 1 run scoreboard players get #fq5G mb
data modify storage rlk:mboss fg.rd5.hold set value 0
function rlk:mboss/fieldgen/fx/tele/dark with storage rlk:mboss fg.rd5
