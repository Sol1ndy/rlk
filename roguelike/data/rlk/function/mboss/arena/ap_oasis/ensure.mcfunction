# 1 when no arena job runs, the box of ap_oasis is loaded, the stamp is "ap_oasis@1:withered" and the sentinel is right.
# Otherwise fail, after making sure a job runs: a wrong / missing version -> build; the right version in another
# look -> the default look job; built but not loaded -> a verify job (waits for the chunks). While another
# arena's job runs nothing starts. Run in minecraft:overworld.
execute if score #mbArBuild mb matches 1.. run return fail
execute unless data storage rlk:mboss {built_ap_oasis:"ap_oasis@1:withered"} run function rlk:mboss/arena/ap_oasis/restore
execute unless data storage rlk:mboss {built_ap_oasis:"ap_oasis@1:withered"} run return fail
execute unless function rlk:mboss/ar/ap_oasis/loaded run function rlk:mboss/arena/ap_oasis/verify
execute if score #mbArBuild mb matches 1.. run return fail
execute unless block 440 193 8 minecraft:packed_mud run function rlk:mboss/arena/ap_oasis/build
execute if score #mbArBuild mb matches 1.. run return fail
return 1
