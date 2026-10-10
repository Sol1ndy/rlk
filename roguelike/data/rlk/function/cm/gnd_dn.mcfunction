scoreboard players add #rl tmp 1
$execute if score #rl tmp matches 48.. run return run function rlk:cm/wd/$(k)
$execute unless block ~ ~-0.05 ~ #rlk:cm_pass positioned ~ ~-0.05 ~ align y positioned ~ ~1 ~ run return run function rlk:cm/wd/$(k)
$execute positioned ~ ~-0.25 ~ run function rlk:cm/gnd_dn {k:"$(k)"}
