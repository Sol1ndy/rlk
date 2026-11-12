# @s = body, #gdTst = the requested test id.
execute if score #gdTst mb matches 1..5 run function rlk:mboss/guardian/test/cut
execute if score #gdTst mb matches 1..5 run scoreboard players operation #gdReq mb = #gdTst mb
execute if score #gdTst mb matches 1..5 run scoreboard players set #gdCool mb 1
execute if score #gdTst mb matches 1..5 run return 0
execute if score #gdTst mb matches 11..13 run function rlk:mboss/guardian/test/cut
execute if score #gdTst mb matches 12 run scoreboard players set #gdSwEl mb 3
execute if score #gdTst mb matches 12 run function rlk:mboss/guardian/rig/spear/electro
execute if score #gdTst mb matches 13 run scoreboard players set #gdFailN mb 2
execute if score #gdTst mb matches 13 run scoreboard players set #gdFailK1 mb 5
execute if score #gdTst mb matches 13 run scoreboard players set #gdFailK2 mb 6
execute if score #gdTst mb matches 11..13 run scoreboard players set #gdSt mb 1
execute if score #gdTst mb matches 11..13 run scoreboard players operation #gdPat mb = #gdTst mb
execute if score #gdTst mb matches 11..13 run return run scoreboard players set #gdPNew mb 1
execute if score #gdTst mb matches 20..21 run function rlk:mboss/guardian/test/cut
execute if score #gdTst mb matches 20 run scoreboard players set #gdSlotA mb 0
execute if score #gdTst mb matches 21 run scoreboard players set #gdSlotA mb 3
execute if score #gdTst mb matches 20 run return run function rlk:mboss/guardian/guard/begin1
execute if score #gdTst mb matches 21 run return run function rlk:mboss/guardian/guard/begin2
execute if score #gdTst mb matches 30..33 run function rlk:mboss/guardian/test/chaos
execute if score #gdTst mb matches 30..33 run return 0
execute if score #gdTst mb matches 40 run function rlk:mboss/guardian/test/cut
execute if score #gdTst mb matches 40 run function rlk:mboss/guardian/rig/play/chaos_fall
execute if score #gdTst mb matches 40 run return run function rlk:mboss/guardian/groggy/begin
execute if score #gdTst mb matches 41 run return run function rlk:mboss/guardian/test/break
execute if score #gdTst mb matches 42 if score #gdTim mb matches 21.. run scoreboard players set #gdTim mb 20
execute if score #gdTst mb matches 42 run return 0
execute if score #gdTst mb matches 91 run scoreboard players set #elem tmp 1
execute if score #gdTst mb matches 92 run scoreboard players set #elem tmp 2
execute if score #gdTst mb matches 93 run scoreboard players set #elem tmp 3
execute if score #gdTst mb matches 94 run scoreboard players set #elem tmp 4
execute if score #gdTst mb matches 91..94 run scoreboard players set #tfm tmp 0
execute if score #gdTst mb matches 91..94 run return run function rlk:mboss/guardian/on_hit
execute if score #gdTst mb matches 99 run return run function rlk:mboss/guardian/test/cut
function rlk:mboss/guardian/test/help
