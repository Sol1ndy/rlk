# Addon dispatcher jump/wave2 (host P2 jump_slam wave2 E 32, called at E - 12 = 20;
# context: the landing point (the anchor); yaw to the player; #azCtxGrp = the wave-2 group). Lines only for the bodies written in this run (s2.md 10.1).
execute if score #azPh mb matches 2.. if score #azLeg mb matches 1 run return run function rlk:mboss/azhdaha/xl/jump_wave2/pyro
