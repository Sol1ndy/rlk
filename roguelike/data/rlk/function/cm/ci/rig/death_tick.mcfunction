function rlk:cm/ci/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 4.. run kill @e[tag=rlk_ci_this]
tag @e[tag=rlk_ci_this] add rlk_cmsync
tag @e[tag=rlk_ci_this] remove rlk_ci_this
