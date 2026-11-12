# 번개 원소 근접 판정 (@s = 두뇌): #cmDmg 설정 후 호출. 플레이어에게 번개가 부착됨
scoreboard players set #cmEl tmp 3
scoreboard players operation #cmLv tmp = @s mlv
function rlk:cm/hit_pl
