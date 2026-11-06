# Hook incoming (@s = body inside combat/apply_mods, after the level factor and mres). NO element RES of any
# kind: mres stays 0 and nothing here reads #elem (every element deals the same). While the field is up
# (#fgOpen 1) the boss takes 60 % ("모든 저항이 증가"), reactions included, at least 1.
execute if score #fgOpen mb matches 1 if score #dmg tmp matches 1.. run function rlk:mboss/fieldgen/field/cut
