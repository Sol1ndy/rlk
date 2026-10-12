# As the shadow (knockback source).
scoreboard players set #cmDmg tmp 6
scoreboard players operation #cmLv tmp = @e[tag=rlk_raiden,limit=1] mlv
scoreboard players set #cmEl tmp 3
function rlk:boss/raiden/hurt
