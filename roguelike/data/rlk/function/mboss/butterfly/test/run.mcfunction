# @s = body, #bfTst = the requested test id.
execute if score #bfTst mb matches 1..4 run function rlk:mboss/butterfly/test/cut
execute if score #bfTst mb matches 1..4 run scoreboard players operation #bfReq mb = #bfTst mb
execute if score #bfTst mb matches 1..4 run scoreboard players set #bfCool mb 1
execute if score #bfTst mb matches 1..4 run return 0
execute if score #bfTst mb matches 11..14 run function rlk:mboss/butterfly/test/cut
execute if score #bfTst mb matches 11..14 run scoreboard players operation #bfReq mb = #bfTst mb
execute if score #bfTst mb matches 11..14 run scoreboard players set #bfCool mb 1
execute if score #bfTst mb matches 11..14 run return 0
execute if score #bfTst mb matches 30 run scoreboard players set #bfTst mb 15
execute if score #bfTst mb matches 15 run function rlk:mboss/butterfly/test/cut
execute if score #bfTst mb matches 15 run scoreboard players set #bfReq mb 15
execute if score #bfTst mb matches 15 run return run scoreboard players set #bfCool mb 1
execute if score #bfTst mb matches 20 run function rlk:mboss/butterfly/test/cut
execute if score #bfTst mb matches 20 run scoreboard players set #bfReq mb 20
execute if score #bfTst mb matches 20 run return run scoreboard players set #bfCool mb 1
execute if score #bfTst mb matches 21 run return run function rlk:mboss/butterfly/coc/apply
execute if score #bfTst mb matches 22 run return run function rlk:mboss/butterfly/test/heal
execute if score #bfTst mb matches 23 run return run function rlk:mboss/butterfly/dew/spawn
execute if score #bfTst mb matches 24 run return run function rlk:mboss/butterfly/coc/clear_hud
execute if score #bfTst mb matches 40 run function rlk:mboss/butterfly/test/cut
execute if score #bfTst mb matches 40 run return run function rlk:mboss/butterfly/groggy/begin
execute if score #bfTst mb matches 42 if score #bfForm mb matches 1 run scoreboard players operation #bfHumN mb = #bfHumLim mb
execute if score #bfTst mb matches 42 if score #bfForm mb matches 2 run scoreboard players operation #bfBfN mb = #bfBfLim mb
execute if score #bfTst mb matches 42 run return 0
execute if score #bfTst mb matches 91 run scoreboard players set #elem tmp 1
execute if score #bfTst mb matches 91 run scoreboard players set #tfm tmp 0
execute if score #bfTst mb matches 91 run return run function rlk:mboss/butterfly/on_hit
execute if score #bfTst mb matches 99 run return run function rlk:mboss/butterfly/test/cut
function rlk:mboss/butterfly/test/help
