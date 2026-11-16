# @s = body, #fgTst = the requested test id.
execute if score #fgTst mb matches 1..6 run function rlk:mboss/fieldgen/test/cut
execute if score #fgTst mb matches 1..6 run scoreboard players operation #fgReq mb = #fgTst mb
execute if score #fgTst mb matches 1..6 run return run scoreboard players set #fgCool mb 1
execute if score #fgTst mb matches 11..12 run function rlk:mboss/fieldgen/test/cut
execute if score #fgTst mb matches 11..12 run scoreboard players operation #fgReq mb = #fgTst mb
execute if score #fgTst mb matches 11..12 run return run scoreboard players set #fgCool mb 1
execute if score #fgTst mb matches 20 run function rlk:mboss/fieldgen/test/cut
execute if score #fgTst mb matches 20 run scoreboard players set #fgReqK mb 0
execute if score #fgTst mb matches 20 run scoreboard players set #fgReq mb 20
execute if score #fgTst mb matches 20 run return run scoreboard players set #fgCool mb 1
execute if score #fgTst mb matches 21 run function rlk:mboss/fieldgen/test/cut
execute if score #fgTst mb matches 21 run scoreboard players set #fgReqK mb 1
execute if score #fgTst mb matches 21 run scoreboard players set #fgReq mb 21
execute if score #fgTst mb matches 21 run return run scoreboard players set #fgCool mb 1
execute if score #fgTst mb matches 22 run function rlk:mboss/fieldgen/test/cut
execute if score #fgTst mb matches 22 run scoreboard players set #fgReqK mb 2
execute if score #fgTst mb matches 22 run scoreboard players set #fgReq mb 21
execute if score #fgTst mb matches 22 run return run scoreboard players set #fgCool mb 1
execute if score #fgTst mb matches 23 run function rlk:mboss/fieldgen/test/cut
execute if score #fgTst mb matches 23 run scoreboard players set #fgReqK mb 0
execute if score #fgTst mb matches 23 run scoreboard players set #fgReq mb 22
execute if score #fgTst mb matches 23 run return run scoreboard players set #fgCool mb 1
execute if score #fgTst mb matches 30 unless score #fgOpen mb matches 1 run function rlk:mboss/fieldgen/test/cut
execute if score #fgTst mb matches 30 unless score #fgOpen mb matches 1 run function rlk:mboss/fieldgen/field/now_f
execute if score #fgTst mb matches 30 run scoreboard players set #fgBrk mb 20
execute if score #fgTst mb matches 30 run return run scoreboard players set #fgBrkQ mb 1
execute if score #fgTst mb matches 31 if score #fgOpen mb matches 1 run scoreboard players add #fgBrk mb 5
execute if score #fgTst mb matches 31 if score #fgBrk mb matches 20.. run scoreboard players set #fgBrk mb 19
execute if score #fgTst mb matches 31 if score #fgOpen mb matches 1 run scoreboard players set #fgBrkFx mb 1
execute if score #fgTst mb matches 31 run return 0
execute if score #fgTst mb matches 40 run function rlk:mboss/fieldgen/test/cut
execute if score #fgTst mb matches 40 run function rlk:mboss/fieldgen/field/drop
execute if score #fgTst mb matches 40 run return run function rlk:mboss/fieldgen/groggy/begin
execute if score #fgTst mb matches 41 run return run function rlk:mboss/fieldgen/test/lowg
execute if score #fgTst mb matches 42 run return run function rlk:mboss/fieldgen/test/tri
execute if score #fgTst mb matches 99 run return run function rlk:mboss/fieldgen/test/cut
function rlk:mboss/fieldgen/test/help
