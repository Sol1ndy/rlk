# 1 when no arena job runs, the box of tk_lift is loaded, the stamp is "tk_lift@1:dust" and the sentinel is right.
# Otherwise fail, after making sure a job runs: a wrong / missing version -> build; the right version in another
# look -> the default look job; built but not loaded -> a verify job (waits for the chunks). While another
# arena's job runs nothing starts. Run in minecraft:overworld.
execute if score #mbArBuild mb matches 1.. run return fail
execute unless data storage rlk:mboss {built_tk_lift:"tk_lift@1:dust"} run function rlk:mboss/arena/tk_lift/restore
execute unless data storage rlk:mboss {built_tk_lift:"tk_lift@1:dust"} run return fail
execute unless function rlk:mboss/ar/tk_lift/loaded run function rlk:mboss/arena/tk_lift/verify
execute if score #mbArBuild mb matches 1.. run return fail
execute unless block 640 196 8 minecraft:polished_deepslate run function rlk:mboss/arena/tk_lift/build
execute if score #mbArBuild mb matches 1.. run return fail
return 1
