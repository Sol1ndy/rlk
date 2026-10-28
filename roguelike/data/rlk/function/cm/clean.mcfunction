function rlk:cm/c2/clean
execute as @e[tag=rlk_sw_anchor,tag=!rlk_cmsync,tag=!rlk_sw_dying] at @s run function rlk:cm/sw/rig/die
execute as @e[tag=rlk_sw_anchor,tag=rlk_sw_dying] at @s run function rlk:cm/sw/rig/death_tick
execute as @e[tag=rlk_ar_anchor,tag=!rlk_cmsync,tag=!rlk_ar_dying] at @s run function rlk:cm/ar/rig/die
execute as @e[tag=rlk_ar_anchor,tag=rlk_ar_dying] at @s run function rlk:cm/ar/rig/death_tick
execute as @e[tag=rlk_fm_anchor,tag=!rlk_cmsync,tag=!rlk_fm_dying] at @s run function rlk:cm/fm/rig/die
execute as @e[tag=rlk_fm_anchor,tag=rlk_fm_dying] at @s run function rlk:cm/fm/rig/death_tick
execute as @e[tag=rlk_im_anchor,tag=!rlk_cmsync,tag=!rlk_im_dying] at @s run function rlk:cm/im/rig/die
execute as @e[tag=rlk_im_anchor,tag=rlk_im_dying] at @s run function rlk:cm/im/rig/death_tick
execute as @e[tag=rlk_sh_anchor,tag=!rlk_cmsync,tag=!rlk_sh_dying] at @s run function rlk:cm/sh/rig/die
execute as @e[tag=rlk_sh_anchor,tag=rlk_sh_dying] at @s run function rlk:cm/sh/rig/death_tick
execute as @e[tag=rlk_cn_anchor,tag=!rlk_cmsync,tag=!rlk_cn_dying] at @s run function rlk:cm/cn/rig/die
execute as @e[tag=rlk_cn_anchor,tag=rlk_cn_dying] at @s run function rlk:cm/cn/rig/death_tick
# 주인(두뇌)이 사라진 모습/부착물 정리. 모습은 쓰러지는 모습을 보이며 사라짐
execute as @e[tag=rlk_cmlink,tag=!rlk_cmsync,tag=rlk_cmv] run function rlk:cm/vis_die
execute as @e[tag=rlk_cmfbh,tag=!rlk_cmsync] at @s run function rlk:cm/fb_fizzle
execute as @e[tag=rlk_cmcbw,tag=!rlk_cmsync] run function rlk:cm/wd_kill
kill @e[tag=rlk_cmlink,tag=!rlk_cmsync,tag=!rlk_sw_dying,tag=!rlk_ar_dying,tag=!rlk_fm_dying,tag=!rlk_im_dying,tag=!rlk_sh_dying,tag=!rlk_cn_dying]
tag @e[tag=rlk_cmsync] remove rlk_cmsync
