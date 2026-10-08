# 아바타가 조준점(rlk_aim)을 바라본다 (@s = 플레이어)
execute as @e[tag=rlk_av,limit=1] at @s anchored eyes facing entity @e[tag=rlk_aim,limit=1] feet run rotate @s ~ ~
