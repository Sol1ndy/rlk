# Cancel bg slot L (selectors only): the emitter's cancel_bg, then the slot ends.
execute if score #azBgL mb matches 31 run function rlk:mboss/azhdaha/p/orbs/cancel_bg
execute if score #azBgL mb matches 43 run function rlk:mboss/azhdaha/p/icicle/cancel_bg
function rlk:mboss/azhdaha/bg/end_l
