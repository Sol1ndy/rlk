# The judge (the final dive's contact; the gauntlet at api.JUDGE_T): #gres hr 1 = the gauge is 0 (the deflect: the
# core starts seq/repel in this tick), 2 = fail (the gauntlet's own branch follows). The gauge is 0 afterwards.
scoreboard players set #gres hr 1
execute if score #gau hr matches 1.. run scoreboard players set #gres hr 2
scoreboard players set #gau hr 0
scoreboard players set #mbDodgeOk mb 0
