# 1 when no arena job runs, the box of cp_test is loaded, the stamp is "cp_test@1:plain" and the sentinel is right.
# Otherwise fail, after making sure a job runs: a wrong / missing version -> build; the right version in another
# look -> the default look job; built but not loaded -> a verify job (waits for the chunks). While another
# arena's job runs nothing starts. Run in minecraft:overworld.
execute if score #mbArBuild mb matches 1.. run return fail
execute unless data storage rlk:mboss {built_cp_test:"cp_test@1:plain"} run function rlk:mboss/arena/cp_test/restore
execute unless data storage rlk:mboss {built_cp_test:"cp_test@1:plain"} run return fail
execute unless function rlk:mboss/ar/cp_test/loaded run function rlk:mboss/arena/cp_test/verify
execute if score #mbArBuild mb matches 1.. run return fail
execute unless block 540 199 8 minecraft:polished_deepslate run function rlk:mboss/arena/cp_test/build
execute if score #mbArBuild mb matches 1.. run return fail
return 1
