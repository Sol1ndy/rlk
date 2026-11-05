# 1 when no arena job runs, the box of hr_field is loaded, the stamp is "hr_field@1:moon" and the sentinel is right.
# Otherwise fail, after making sure a job runs: a wrong / missing version -> build; the right version in another
# look -> the default look job; built but not loaded -> a verify job (waits for the chunks). While another
# arena's job runs nothing starts. Run in minecraft:overworld.
execute if score #mbArBuild mb matches 1.. run return fail
execute unless data storage rlk:mboss {built_hr_field:"hr_field@1:moon"} run function rlk:mboss/arena/hr_field/restore
execute unless data storage rlk:mboss {built_hr_field:"hr_field@1:moon"} run return fail
execute unless function rlk:mboss/ar/hr_field/loaded run function rlk:mboss/arena/hr_field/verify
execute if score #mbArBuild mb matches 1.. run return fail
execute unless block 880 196 8 minecraft:polished_tuff run function rlk:mboss/arena/hr_field/build
execute if score #mbArBuild mb matches 1.. run return fail
return 1
