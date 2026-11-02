# Hook resume (@s = body): the pattern's redraw (decals with the ticks left, prop looks), the banner inside a
# break window, the badge (hud/sub).
execute if score #pat kn matches 3 run function rlk:boss/arlecchino/p/b1/resume
execute if score #pat kn matches 4 run function rlk:boss/arlecchino/p/b2/resume
execute if score #pat kn matches 10 run function rlk:boss/arlecchino/p/f1/resume
execute if score #pat kn matches 11 run function rlk:boss/arlecchino/p/g1/resume
execute if score #pat kn matches 12 run function rlk:boss/arlecchino/p/h1/resume
execute if score #pat kn matches 20 run function rlk:boss/arlecchino/p/e70/resume
execute if score #win kn matches 1 run function rlk:boss/arlecchino/fx/hud/banner {on:1}
function rlk:boss/arlecchino/hud/sub
