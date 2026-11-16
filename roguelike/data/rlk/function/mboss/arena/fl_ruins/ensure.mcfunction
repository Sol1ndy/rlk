# 1 when no arena job runs, the box of fl_ruins is loaded, the stamp is "fl_ruins@1:day" and the sentinel is right.
# Otherwise fail, after making sure a job runs: a wrong / missing version -> build; the right version in another
# look -> the default look job; built but not loaded -> a verify job (waits for the chunks). While another
# arena's job runs nothing starts. Run in minecraft:overworld.
execute if score #mbArBuild mb matches 1.. run return fail
execute unless data storage rlk:mboss {built_fl_ruins:"fl_ruins@1:day"} run function rlk:mboss/arena/fl_ruins/restore
execute unless data storage rlk:mboss {built_fl_ruins:"fl_ruins@1:day"} run return fail
execute unless function rlk:mboss/ar/fl_ruins/loaded run function rlk:mboss/arena/fl_ruins/verify
execute if score #mbArBuild mb matches 1.. run return fail
execute unless block 760 196 8 minecraft:polished_deepslate run function rlk:mboss/arena/fl_ruins/build
execute if score #mbArBuild mb matches 1.. run return fail
return 1
