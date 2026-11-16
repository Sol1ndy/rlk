# /reload: the proxy state again from #azPx.
execute if score #azPx mb matches 0 run return run function rlk:boss/azhdaha/px/normal
execute if score #azPx mb matches 1 run return run function rlk:boss/azhdaha/px/jump
execute if score #azPx mb matches 2 run return run function rlk:boss/azhdaha/px/inv
execute if score #azPx mb matches 3 run return run function rlk:boss/azhdaha/px/tail_only
execute if score #azPx mb matches 4 run return run function rlk:boss/azhdaha/px/dead
