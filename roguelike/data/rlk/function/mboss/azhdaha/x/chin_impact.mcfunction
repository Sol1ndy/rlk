# Addon dispatcher chin/impact (host P1 chin_slam impact E 35, called at E - 12 = 23;
# context: the impact point; yaw of the crack line (anchor -> impact); #azCtxGrp). Lines only for the bodies written in this run (s2.md 10.1).
execute if score #azPh mb matches 2.. if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/xl/chin_impact/hydro
execute if score #azPh mb matches 2.. if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/xl/chin_impact/pyro
execute if score #azPh mb matches 3 if score #azTail mb matches 4 run function rlk:mboss/azhdaha/xt/chin_impact/cryo
execute if score #azPh mb matches 3 if score #azTail mb matches 3 run function rlk:mboss/azhdaha/xt/chin_impact/electro
