# Hook incoming (@s = body inside combat/apply_mods; the framework floor runs after it): damage taken x #taken %
# (100; mantle 20, stun 150, G3 stagger 130).
execute if score #taken tk matches 100 run return 0
scoreboard players operation #dmg tmp *= #taken tk
scoreboard players operation #dmg tmp /= #c100 tk
