# Navia skill_aim fx (owner: skill; loop): a flickering horizontal lens glint at the ferrule while aiming
# (gameplay char/navia/aim_tick adds the ambient wax sparkles). ^left ^up ^forward, pitch 0.
execute if score @s pmTick matches 2 run function rlk:char/motion/navia_fx/skill_aim/t002
execute if score @s pmTick matches 5 run function rlk:char/motion/navia_fx/skill_aim/t005
execute if score @s pmTick matches 7 run function rlk:char/motion/navia_fx/skill_aim/t007
execute if score @s pmTick matches 12 run function rlk:char/motion/navia_fx/skill_aim/t012
execute if score @s pmTick matches 15 run function rlk:char/motion/navia_fx/skill_aim/t015
execute if score @s pmTick matches 17 run function rlk:char/motion/navia_fx/skill_aim/t017
