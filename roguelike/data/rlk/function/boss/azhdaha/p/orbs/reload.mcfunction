# /reload with the orbs in bg slot L: every aux entity is gone; re-make them at their angles (elapsed
# steps = the bg clock + 1) in a new volley group; a fading orbit just ends.
execute if score #azBgLT mb >= #aq31E mb run return run function rlk:boss/azhdaha/p/orbs/end
execute at @s run function rlk:boss/azhdaha/p/orbs/remake
