# Hook on_hit (@s = body inside combat/apply, before apply_mods; scores only): a skill / burst hit flags the A6 trigger
# (#skillDmg tmp 1; resolved by the next fight tick), a hit while she recovers / idles feeds the counter trigger. HA-02:
# none of it while the balance groggy runs (grgT; the punish window queues no reaction).
execute if score @s grgT matches 1.. run return 0
execute if score #skillDmg tmp matches 1 run scoreboard players set #a6q hr 1
execute if score #pat hr matches 0 if score #ph hr matches 1 run function rlk:boss/scarlet/core/hit_rec
execute if score #pat hr matches 0 if score #ph hr matches 7 run function rlk:boss/scarlet/core/hit_rec
