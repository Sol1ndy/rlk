# Gold sweep (guard timeout) tick (@s = body, #gdPT = clip tick).
execute if score #gdPT mb matches 1..18 run return run function rlk:mboss/guardian/p/sweep_g/d/1_18
execute if score #gdPT mb matches 19..44 run return run function rlk:mboss/guardian/p/sweep_g/d/19_44
