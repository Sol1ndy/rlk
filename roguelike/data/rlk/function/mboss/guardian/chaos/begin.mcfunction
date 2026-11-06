# @s = body. Chaos (K10): leap + arcing flight to the centre (from >= 6 b), else a short glide; landing;
# charge with the spear level; rise to the hover; then the 350 t timer and the two stars.
scoreboard players set #gdSt mb 4
scoreboard players set #gdT mb 0
scoreboard players set #gdCP mb 1
scoreboard players set #mbNoLeash mb 1
scoreboard players set #gdBrk mb 0
scoreboard players set #gdFailDone mb 0
scoreboard players set #gdStars mb 0
function rlk:mboss/guardian/rig/eye/red
scoreboard players set #gdChV mb 1
execute if entity @e[tag=rlk_mb_arena,distance=..6,limit=1] run scoreboard players set #gdChV mb 2
execute if score #gdChV mb matches 1 at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #gdChV mb matches 1 run function rlk:mboss/guardian/rig/play/chaos_leap
execute if score #gdChV mb matches 1 run playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.27
execute if score #gdChV mb matches 1 run playsound minecraft:item.elytra.flying hostile @a[tag=player] ~ ~ ~ 0.4 1.3 0.13
execute if score #gdChV mb matches 1 run particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~1 ~ 0.6 0.6 0.6 0 16 force @a[tag=player]
execute if score #gdChV mb matches 2 run function rlk:mboss/guardian/rig/play/glide
execute if score #gdChV mb matches 2 run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.2
function rlk:mboss/guardian/hud/sub_chaos_in
