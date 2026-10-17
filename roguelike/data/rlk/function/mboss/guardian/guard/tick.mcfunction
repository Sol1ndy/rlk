scoreboard players add #gdT mb 1
execute if score #gdGP mb matches 1 run return run function rlk:mboss/guardian/guard/entry
execute if score #gdGP mb matches 2 run return run function rlk:mboss/guardian/guard/active
execute if score #gdGP mb matches 4 run return run function rlk:mboss/guardian/guard/gap
# phase 3: the sweep pattern runs in the slot (guard/after when it ends)
