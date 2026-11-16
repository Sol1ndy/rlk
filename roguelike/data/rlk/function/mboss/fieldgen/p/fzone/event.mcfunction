# One eruption event (@s = body): 1-4 discs, the first 2-3 b off the player, the others 2-8 b; one volley group.
function rlk:mboss/grp_new
execute store result score #fq11N mb run random value 1..4
execute store result storage rlk:mboss fg.fz.d double 0.1 run random value 20..30
scoreboard players set #fq11F mb 1
function rlk:mboss/fieldgen/p/fzone/disc
function rlk:mboss/fieldgen/p/fzone/more
