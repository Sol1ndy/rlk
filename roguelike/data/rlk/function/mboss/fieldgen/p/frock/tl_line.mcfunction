# @s = the slab about to be thrown, at it (its throw in 10 t): it flares on itself (kit p/slab_glint) with a
# chain clink. No lane or line on the floor (telegraph rule 10-20: the footage's slabs are flung with streaks).
function rlk:mboss/fieldgen/fx/p/slab_glint
playsound minecraft:block.chain.hit hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
