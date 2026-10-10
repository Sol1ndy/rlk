# 근접 공격 판정 (@s = 두뇌): #cmDmg 설정 후 호출
scoreboard players set #cmEl tmp 0
scoreboard players operation #cmLv tmp = @s mlv
function rlk:cm/hit_pl
