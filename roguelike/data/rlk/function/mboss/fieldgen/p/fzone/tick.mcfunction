# fzone tick: track the player (3 deg/t), the decals again after a pause.
function rlk:mboss/mv/turn {max:3}
execute if score #fq11P mb matches 1 run function rlk:mboss/fieldgen/p/fzone/redraw
execute if score #fgPT mb matches 6..142 run return run function rlk:mboss/fieldgen/p/fzone/d/6_142
execute if score #fgPT mb matches 160..271 run return run function rlk:mboss/fieldgen/p/fzone/d/160_271
