# P3 tick (#azPT = the charge_coil clip tick; the coil chains into charge_run by itself)
execute if score #aq3R mb matches 1 run function rlk:mboss/azhdaha/p/charge/run
execute if score #aq3K mb matches 1.. run function rlk:mboss/azhdaha/p/charge/skid
execute if score #aq3H mb matches 1 run function rlk:mboss/azhdaha/p/charge/follow
execute if score #aq3E mb matches 1.. if score #azPT mb >= #aq3E mb run function rlk:mboss/azhdaha/p/end
execute if score #azPT mb matches 0..7 run return run function rlk:mboss/azhdaha/p/charge/kd/0_7
execute if score #azPT mb matches 8..24 run return run function rlk:mboss/azhdaha/p/charge/kd/8_24
