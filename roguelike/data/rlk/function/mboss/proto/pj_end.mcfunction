# Hook pj_end (@s = projectile prop, #pjEv 1 wall / 2 life / 3 back at the body / 4 hit the player).
execute if score #pjEv mb matches 3 at @s run particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.1 6 force @a[tag=player]
