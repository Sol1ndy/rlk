# The impact visual (t35) at the impact point: blade crown, crack fan, sound, flash (the dust ring follows
# 1 t later: one tick of four card presets passed the 3000-command perf budget).
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/crown/1
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/crown/2
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/crown/3
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/crown/4
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/crown/5
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/cracks/1 {r:56}
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/cracks/2 {r:56}
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/cracks/3 {r:56}
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/cracks/4 {r:56}
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/cracks/5 {r:56}
function rlk:boss/azhdaha/fx/snd/chin_impact
function rlk:boss/azhdaha/fx/hud/flash_amber
