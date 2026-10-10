# One successful contact per rush; keep cmS=3 and the remaining movement steps.
scoreboard players operation #cmDmg tmp = #cmD_shR tmp
function rlk:cm/hit_me
execute unless score #dodged tmp matches 1 run tag @s add rlk_sh_rhit
