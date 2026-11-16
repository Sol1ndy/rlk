# 번개 시킨 (@s = small NoAI brain, at @s). Orbits the body at ~4 b; when its caster picks it: 0.5 s glow
# + vex cue, then a straight ram at the chest (8, electro). Owned ones are linked to the caster (cm/clean removes
# them with it); a test-spawned one (/function rlk:cm/test {t:"ci"}) is its own brain and rams on its own timer.
function rlk:cm/ci/lib/pre
execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/ci/reset
execute if score @s frzT matches 1.. if score @s cmS matches 1.. run function rlk:cm/ci/idle
execute if score @s frzT matches 1.. run return 0
execute if score @s cmS matches 1 run return run function rlk:cm/ci/r_tell
execute if score @s cmS matches 2 run return run function rlk:cm/ci/r_fly
execute if score @s cmS matches 3 run function rlk:cm/ci/r_back
function rlk:cm/ci/orbit
execute if score @s c2eOw matches 0 if score @s cmS matches 0 if score @s cmCd matches ..0 if score #free tmp matches 1 run function rlk:cm/ci/r_start
