# Addon dispatcher jump/land (host P2 jump_slam land E 21, called at E - 12 = 9;
# context: the landing point; yaw to the player; #azCtxGrp = the landing group). Lines only for the bodies written in this run (s2.md 10.1).
execute if score #azPh mb matches 2.. if score #azLeg mb matches 2 run return run function rlk:mboss/azhdaha/xl/jump_land/hydro
execute if score #azPh mb matches 3 if score #azTail mb matches 4 run function rlk:mboss/azhdaha/xt/jump_land/cryo
