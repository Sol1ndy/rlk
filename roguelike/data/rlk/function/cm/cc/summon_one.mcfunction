function rlk:cm/spawn/ci
$execute as @e[tag=rlk_cm_ci] if score @s cmId = #cmIdC tmp run function rlk:cm/cc/ci_own {a:$(a)}
