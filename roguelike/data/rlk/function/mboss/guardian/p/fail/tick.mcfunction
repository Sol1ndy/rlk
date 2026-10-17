# Fail spears tick (@s = body, #gdPT = ticks since T0).
execute unless score #gdFailN mb matches 1.. run return run function rlk:mboss/guardian/p/end
execute if score #gdPT mb matches 17..53 run return run function rlk:mboss/guardian/p/fail/d/17_53
execute if score #gdPT mb matches 54..93 run return run function rlk:mboss/guardian/p/fail/d/54_93
