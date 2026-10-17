# Fail spears tick (@s = body, #gdPT = ticks since T0).
execute unless score #gdFailN mb matches 1.. run return run function rlk:mboss/guardian/p/end
execute if score #gdPT mb matches 23..64 run return run function rlk:mboss/guardian/p/fail/d/23_64
execute if score #gdPT mb matches 65..113 run return run function rlk:mboss/guardian/p/fail/d/65_113
