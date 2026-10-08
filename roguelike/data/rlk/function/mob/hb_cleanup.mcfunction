# 체력바/빙결 정리 (주인 잃은 것 제거). 몹 또는 체력바가 존재할 때만 호출됨(메인 tick 게이팅)
execute as @e[tag=rlk_mob] on passengers run tag @s add rlk_hb_ok
kill @e[tag=rlk_hb_bg,tag=!rlk_hb_ok]
kill @e[tag=rlk_hb_fg,tag=!rlk_hb_ok]
tag @e[tag=rlk_hb_bg] remove rlk_hb_ok
tag @e[tag=rlk_hb_fg] remove rlk_hb_ok
kill @e[tag=rlk_hb_num,tag=!rlk_hb_ok]
tag @e[tag=rlk_hb_num] remove rlk_hb_ok
kill @e[tag=rlk_hb_lv,tag=!rlk_hb_ok]
tag @e[tag=rlk_hb_lv] remove rlk_hb_ok
kill @e[tag=rlk_hb_icon,tag=!rlk_hb_ok]
tag @e[tag=rlk_hb_icon] remove rlk_hb_ok
execute as @e[tag=rlk_mob] if score @s frzT matches 1.. on passengers if entity @s[tag=rlk_frz_ice] run tag @s add rlk_frz_ok
kill @e[tag=rlk_frz_ice,tag=!rlk_frz_ok]
tag @e[tag=rlk_frz_ice] remove rlk_frz_ok
kill @e[tag=rlk_hb_er,tag=!rlk_hb_ok]
tag @e[tag=rlk_hb_er] remove rlk_hb_ok
