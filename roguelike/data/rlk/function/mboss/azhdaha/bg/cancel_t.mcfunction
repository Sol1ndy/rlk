# Cancel bg slot T (selectors only): the emitter's cancel_bg, then the slot ends.
execute if score #azBgT mb matches 31 run function rlk:mboss/azhdaha/p/orbs/cancel_bg
execute if score #azBgT mb matches 43 run function rlk:mboss/azhdaha/p/icicle/cancel_bg
function rlk:mboss/azhdaha/bg/end_t
