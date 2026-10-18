scoreboard players add #bfT mb 1
execute if score #bfT mb matches 1..24 run function rlk:mboss/mv/turn {max:9}
execute if score #bfT mb matches 24 run function rlk:mboss/butterfly/rig_stub/play/chain_reform
function rlk:mboss/butterfly/seq_h/recover/tick
execute if score #bfT mb matches 42.. run function rlk:mboss/butterfly/groggy/end
