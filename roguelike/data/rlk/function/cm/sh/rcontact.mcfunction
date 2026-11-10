# One successful contact per rush; keep cmS=3 and the remaining movement steps.
scoreboard players operation #cmDmg tmp = #cmD_shR tmp
function rlk:cm/hit_me
execute unless score #dodged tmp matches 1 run tag @s add rlk_sh_rhit
# 퍼펙트 패링으로 막은 돌진도 끝남(닷지로 피하면 계속 달림)
execute if score #parT tmp matches 3 run tag @s add rlk_sh_rhit
