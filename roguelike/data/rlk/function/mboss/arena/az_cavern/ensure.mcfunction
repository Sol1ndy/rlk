# 1 when no arena job runs, the box of az_cavern is loaded, the stamp is "az_cavern@2:default" and the sentinel is right.
# Otherwise fail, after making sure a job runs: a wrong / missing version -> build; the right version in another
# look -> the default look job; built but not loaded -> a verify job (waits for the chunks). While another
# arena's job runs nothing starts. Run in minecraft:overworld.
execute if score #mbArBuild mb matches 1.. run return fail
execute unless data storage rlk:mboss {built_az_cavern:"az_cavern@2:default"} run function rlk:mboss/arena/az_cavern/restore
execute unless data storage rlk:mboss {built_az_cavern:"az_cavern@2:default"} run return fail
execute unless function rlk:mboss/ar/az_cavern/loaded run function rlk:mboss/arena/az_cavern/verify
execute if score #mbArBuild mb matches 1.. run return fail
execute unless block 320 195 8 minecraft:smooth_basalt run function rlk:mboss/arena/az_cavern/build
execute if score #mbArBuild mb matches 1.. run return fail
return 1
