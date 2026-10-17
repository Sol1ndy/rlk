# Fail spears tick (@s = body, #gdPT = ticks since T0).
execute unless score #gdFailN mb matches 1.. run return run function rlk:mboss/guardian/p/end
execute if score #gdPT mb matches 23..65 run return run function rlk:mboss/guardian/p/fail/d/23_65
execute if score #gdPT mb matches 66..113 run return run function rlk:mboss/guardian/p/fail/d/66_113
