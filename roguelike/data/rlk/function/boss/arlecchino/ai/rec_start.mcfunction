# Recovery start (@s = body, after a pattern / stun / transition): idle 16-24 t (P2 12-18) facing the player - the
# punish window, the scythe low: walk in (0.12 b/t) when farther than 6 b, else strafe (random side).
execute if score #ph kn matches 1 store result score #rec kn run random value 16..24
execute if score #ph kn matches 3 store result score #rec kn run random value 16..24
execute if score #ph kn matches 5 store result score #rec kn run random value 12..18
execute if score #ai_d2 kn matches 360001.. run scoreboard players set #ai_mv kn 1
execute if score #ai_d2 kn matches 360001.. run return run function rlk:boss/arlecchino/ai/play_walk
execute store result score #ai_mv kn run random value 2..3
function rlk:boss/arlecchino/ai/play_strafe
