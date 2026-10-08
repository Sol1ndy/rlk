# @s = 오브젝트. 조준 시작/끝에 안내 글자 표시/숨김
execute if entity @s[tag=rlk_ohover,tag=!rlk_ohov_on] run function rlk:room/obj/hover_on
execute if entity @s[tag=!rlk_ohover,tag=rlk_ohov_on] run function rlk:room/obj/hover_off
