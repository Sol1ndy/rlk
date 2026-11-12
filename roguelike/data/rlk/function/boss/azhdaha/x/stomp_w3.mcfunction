# Addon dispatcher stomp/w3 (host P5 stomp_fl w3 E 47, called at E - 12 = 35;
# context: the paw point; yaw to the player; #azCtxPaw, #azCtxGrp = w3's group). Lines only for the bodies written in this run (s2.md 10.1).
execute if score #azPh mb matches 2.. if score #azLeg mb matches 1 run function rlk:boss/azhdaha/xl/stomp_w3/pyro
execute if score #azPh mb matches 3 if score #azTail mb matches 3 run function rlk:boss/azhdaha/xt/stomp_w3/electro
