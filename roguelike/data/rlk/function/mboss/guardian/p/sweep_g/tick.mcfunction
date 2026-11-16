# Gold sweep (guard timeout) tick (@s = body, #gdPT = clip tick).
execute if score #gdPT mb matches 1..16 run return run function rlk:mboss/guardian/p/sweep_g/d/1_16
execute if score #gdPT mb matches 17..39 run return run function rlk:mboss/guardian/p/sweep_g/d/17_39
