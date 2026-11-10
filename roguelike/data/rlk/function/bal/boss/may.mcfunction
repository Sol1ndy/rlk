# @s = boss: may it take balance damage now? Registry bosses: only in the fight state, outside cutscenes and hidden
# bars (scarlet cines); Raiden: the Shogun phase only (Tenma's armour is its gauge), not in the transformation,
# the exhausted / stunned / finishing states, a blink or the death
execute if entity @s[tag=rlk_mb_body] unless score #mbSt mb matches 1 run return fail
execute if entity @s[tag=rlk_mb_body] if score #mbCine mb matches 1 run return fail
execute if entity @s[tag=rlk_mb_body] if score #mbBarOff mb matches 1 run return fail
execute if entity @s[tag=rlk_mb_dying] run return fail
execute if entity @s[tag=rlk_raiden] unless score @s rdPhase matches 0 run return fail
execute if entity @s[tag=rlk_raiden] if score @s rdDeath matches 1.. run return fail
execute if entity @s[tag=rlk_raiden] if score @s rdPat matches 98..99 run return fail
return 1
