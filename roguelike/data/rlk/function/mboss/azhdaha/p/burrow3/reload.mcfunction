# The B3 resumes at its frame tick #azPT (plan 4.3; tests 25 / 61 start here): the proxy state, the rig clip, the
# anchor at the centre after the glide, #azBur, the special (re-made from the current B3 tick, or started), the crater.
scoreboard players operation #azB3T mb = #azPT mb
scoreboard players set #mbNoLeash mb 1
execute if score #azPT mb matches 40..417 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run tp @s ~ ~ ~
# (FIX STATE-4: from the glide's start: the body is hidden from t40, the stopped glide would leave it off-centre)
execute if score #azPT mb matches ..7 run function rlk:mboss/azhdaha/px/normal
execute if score #azPT mb matches 8..57 run function rlk:mboss/azhdaha/px/inv
execute if score #azPT mb matches 58..334 run function rlk:mboss/azhdaha/px/tail_only
execute if score #azPT mb matches 335..417 run function rlk:mboss/azhdaha/px/inv
execute if score #azPT mb matches 418.. run function rlk:mboss/azhdaha/px/normal
execute if score #azPT mb matches ..65 run function rlk:mboss/azhdaha/rig/play/p3_sink
execute if score #azPT mb matches 66..334 run function rlk:mboss/azhdaha/rig/play/tail_pillar
execute if score #azPT mb matches 335..379 run function rlk:mboss/azhdaha/rig/play/tail_pillar_sink
execute if score #azPT mb matches 380.. run function rlk:mboss/azhdaha/rig/play/burrow_emerge
scoreboard players set #azBur mb 0
execute if score #azPT mb matches 58..417 run scoreboard players set #azBur mb 1
execute if score #azPT mb matches 58..387 if score #azB3Sp mb matches 1.. run function rlk:mboss/azhdaha/b3/special_reload
execute if score #azPT mb matches 58..387 unless score #azB3Sp mb matches 1.. run function rlk:mboss/azhdaha/b3/special_start
execute if score #azPT mb matches 360..387 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/p/burrow3/emerge_r
execute if score #azPT mb matches ..417 run function rlk:mboss/azhdaha/p/burrow3/crater
