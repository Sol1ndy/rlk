scoreboard players add #bfT mb 1
# still debuffed after 달빛 해제: one new 달빛 이슬 during the groggy
execute if score #bfT mb matches 20 if score #bfCoc mb matches 1 run function rlk:mboss/butterfly/dew/spawn1
function rlk:mboss/butterfly/seq_h/groggy/tick
execute if score #bfT mb matches 300.. run function rlk:mboss/butterfly/recover/begin
