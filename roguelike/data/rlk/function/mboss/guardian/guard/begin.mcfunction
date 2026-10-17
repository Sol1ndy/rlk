# @s = body. Guard mode #gdGN (1 = slot A, 2 = slot B): entry twirl (50 t), then 100 t of record window.
scoreboard players set #gdSt mb 3
scoreboard players set #gdT mb 0
scoreboard players set #gdGP mb 1
scoreboard players set #gdRecOn mb 0
scoreboard players set #gdRecNew mb 0
scoreboard players set #gdRecEl mb 0
scoreboard players set #gdN1 mb 0
scoreboard players set #gdQ1 mb 3
scoreboard players set #gdRc1 mb 0
execute if score #gdGN mb matches 2 if score #gdSlotA mb matches 1 run scoreboard players set #gdQ1 mb 9
scoreboard players set #gdN2 mb 0
scoreboard players set #gdQ2 mb 3
scoreboard players set #gdRc2 mb 0
execute if score #gdGN mb matches 2 if score #gdSlotA mb matches 2 run scoreboard players set #gdQ2 mb 9
scoreboard players set #gdN3 mb 0
scoreboard players set #gdQ3 mb 3
scoreboard players set #gdRc3 mb 0
execute if score #gdGN mb matches 2 if score #gdSlotA mb matches 3 run scoreboard players set #gdQ3 mb 9
scoreboard players set #gdN4 mb 0
scoreboard players set #gdQ4 mb 3
scoreboard players set #gdRc4 mb 0
execute if score #gdGN mb matches 2 if score #gdSlotA mb matches 4 run scoreboard players set #gdQ4 mb 9
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/guard_entry
function rlk:mboss/guardian/look/eye_guard
function rlk:mboss/guardian/voice/guard
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.3
function rlk:mboss/guardian/hud/sub_guard
