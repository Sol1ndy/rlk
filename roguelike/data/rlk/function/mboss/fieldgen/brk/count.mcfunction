# @s = body (module tick after a counted hit): the crack stage (hits 0-4 / 5-9 / 10-14 / 15-19 = 0-3), the crack
# glint and the chime at the core, the newest pip flashes for 4 t.
scoreboard players set #fgBrkFx mb 0
scoreboard players operation #fgX mb = #fgBrk mb
scoreboard players operation #fgX mb /= #fgK5 mb
execute if score #fgX mb matches 4.. run scoreboard players set #fgX mb 3
execute unless score #fgX mb = #fgCrack mb run function rlk:mboss/fieldgen/brk/stage
function rlk:mboss/fieldgen/cfx/count
scoreboard players set #fgPipT mb 4
function rlk:mboss/fieldgen/hud/refresh
