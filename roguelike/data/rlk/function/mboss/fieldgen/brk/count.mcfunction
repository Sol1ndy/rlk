# @s = body (module tick after a counted hit): the crack stage (hits 0-4 / 5-9 / 10-14 / 15-19 = 0-3); the
# kit's per-count feedback with #fkM = the count, as the body (the rig anchor) at the field core
# (4.1 b up): the newest pip flashes white for 4 t, the crack glint, the brass ping + a note rising
# with the count, and at 5 / 10 / 15 the bubble crack fx, its sound and the rig crack/<n>.
scoreboard players set #fgBrkFx mb 0
scoreboard players operation #fgX mb = #fgBrk mb
scoreboard players operation #fgX mb /= #fgK5 mb
execute if score #fgX mb matches 4.. run scoreboard players set #fgX mb 3
execute unless score #fgX mb = #fgCrack mb run function rlk:mboss/fieldgen/brk/stage
scoreboard players operation #fkM mb = #fgBrk mb
execute positioned ~ ~4.1 ~ run function rlk:mboss/fieldgen/fx/hud/meter_hit
function rlk:mboss/fieldgen/hud/refresh
