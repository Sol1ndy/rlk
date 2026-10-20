# Addon dispatcher jump/wave2 (host P2 jump_slam wave2 E 32, called at E - 12 = 20;
# context: the landing point (the anchor); yaw to the player; #azCtxGrp = the wave-2 group). Lines only for the bodies written in this run (s2.md 10.1).
execute if score #azPh mb matches 3 if score #azTail mb matches 3 run function rlk:mboss/azhdaha/xt/jump_wave2/electro
