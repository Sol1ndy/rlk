# Hook death_tick (@s = body, #mbT 1.. until cur.death): the clip (rig tick), seq/death beats, the arena wave.
function rlk:boss/azhdaha/rig/tick
function rlk:boss/azhdaha/seq/death/tick
scoreboard players operation #azM mb = #mbT mb
scoreboard players operation #azM mb %= #azK4 mb
execute if score #azM mb matches 0 if score #azArT mb matches 1.. run function rlk:boss/azhdaha/arena/wave
