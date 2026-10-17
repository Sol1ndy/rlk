# On the centre star: landing (the heaviest boom of the fight for the leap), facing the player.
scoreboard players set #gdCP mb 2
scoreboard players operation #gdCh0 mb = #gdT mb
function rlk:mboss/guardian/rig/face/player
execute if score #gdChV mb matches 1 run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.3
execute if score #gdChV mb matches 1 run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.5 0.5 0.3
execute if score #gdChV mb matches 1 run function rlk:fx/nv/card {kind:"ring",pos:"~ ~0.1 ~",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1,s1:7,move:"0f,0f,0f",life:8,fade:3}
execute if score #gdChV mb matches 1 run particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~0.3 ~ 1.6 0.2 1.6 0 30 force @a[tag=player]
execute if score #gdChV mb matches 2 run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1 0.3
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.3
