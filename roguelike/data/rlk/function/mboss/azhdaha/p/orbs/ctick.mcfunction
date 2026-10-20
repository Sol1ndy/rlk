# Cast clock #azCT: t60 the orbs spawn, then bg slot L takes them and the cast slot ends.
execute if score #azCT mb matches 60 run function rlk:mboss/azhdaha/p/orbs/spawn
execute if score #azCT mb matches 60 run function rlk:mboss/azhdaha/bg/start_l
execute if score #azCT mb matches 60.. run function rlk:mboss/azhdaha/cast/end
