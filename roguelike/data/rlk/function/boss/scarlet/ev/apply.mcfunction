# The grant (seq/event at E56, or the reward hook for a cut coda; @s any): once per kill, as the player.
execute if score #hrEvDone hr matches 1 run return 0
execute unless score #hrEv hr matches 1..2 run function rlk:boss/scarlet/ev/roll
scoreboard players set #hrEvDone hr 1
execute if score #hrEv hr matches 1 as @a[tag=player,limit=1] run function rlk:boss/scarlet/ev/item
execute if score #hrEv hr matches 2 as @a[tag=player,limit=1] run function rlk:boss/scarlet/ev/buff
