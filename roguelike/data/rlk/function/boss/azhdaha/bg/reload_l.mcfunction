# /reload with bg slot L live: the emitter re-makes its props (reload), else it ends.
execute if score #azBgL mb matches 31 run return run function rlk:boss/azhdaha/p/orbs/reload
execute if score #azBgL mb matches 43 run return run function rlk:boss/azhdaha/p/icicle/reload
function rlk:boss/azhdaha/bg/end_l
