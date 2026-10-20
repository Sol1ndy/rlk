# 잠복 돌진 (burrow, id 9) - tick
execute if score #azPT mb matches 41..94 run function rlk:mboss/azhdaha/p/burrow/under
execute if score #azPT mb matches 126..164 run function rlk:mboss/azhdaha/p/burrow/under
execute if score #azPT mb matches 196..219 run function rlk:mboss/azhdaha/p/burrow/under
execute if score #aq9E mb matches 1 if score #azPT mb matches 259.. if score #aq9R mb matches 1.. run function rlk:mboss/azhdaha/p/burrow/run_step
execute if score #aq9E mb matches 1 if score #aq9X mb matches 1.. if score #azPT mb >= #aq9X mb run return run function rlk:mboss/azhdaha/p/burrow/fin
execute if score #azPT mb matches 3..122 run return run function rlk:mboss/azhdaha/p/burrow/kd/3_122
execute if score #azPT mb matches 123..273 run return run function rlk:mboss/azhdaha/p/burrow/kd/123_273
