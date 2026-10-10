# @s = 오브젝트. 조준 시작/끝에 안내 글자
execute if entity @s[tag=rlk_lhover,tag=!rlk_lhov_on] run function rlk:lobby/obj/hover_on
execute if entity @s[tag=!rlk_lhover,tag=rlk_lhov_on] run function rlk:lobby/obj/hover_off
