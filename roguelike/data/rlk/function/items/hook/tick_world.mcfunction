# 아이템 소환물/투사체 매 틱 처리 (루트 tick 에서 호출). 존재할 때만
execute as @e[tag=rlk_page_orb] at @s run function rlk:items/proc/page_orb_tick
execute if entity @e[tag=rlk_kslash,limit=1] as @e[tag=rlk_kslash] at @s run function rlk:items/proc/kslash_tick
execute as @e[tag=rlk_eyeq] at @s run function rlk:items/proc/eye_strike
execute as @e[tag=rlk_pot] at @s run function rlk:items/proc/pot_tick
execute as @e[tag=rlk_flag] at @s run function rlk:items/proc/flag_tick
execute as @e[tag=rlk_quillq] at @s run function rlk:items/proc/quill_hit
execute as @e[tag=rlk_decoym] at @s run function rlk:items/proc/bunny_tick
execute as @e[tag=rlk_blossom] at @s run function rlk:items/proc/blossom_tick
execute as @e[tag=rlk_blq] at @s run function rlk:items/proc/blossom_hit
execute as @e[tag=rlk_iq] at @s run function rlk:items/q/run
execute as @e[tag=rlk_jelly] at @s run function rlk:items/proc/jelly_tick
execute as @e[tag=rlk_gflag] at @s run function rlk:items/proc/gflag_tick
execute as @e[tag=rlk_doll] at @s run function rlk:items/proc/doll_tick
execute as @e[tag=rlk_wisp] at @s run function rlk:items/proc/wisp_tick
execute as @e[tag=rlk_hound] at @s run function rlk:items/proc/hound_tick
execute as @e[tag=rlk_vortex] at @s run function rlk:items/proc/vortex_tick
execute as @e[tag=rlk_sakura] at @s run function rlk:items/proc/sakura_tick
execute as @e[tag=rlk_storm] at @s run function rlk:items/proc/storm_tick
execute as @e[tag=rlk_meteor] at @s run function rlk:items/proc/meteor_tick
execute as @e[tag=rlk_case] at @s run function rlk:items/proc/case_tick
execute as @e[tag=rlk_tengu] at @s run function rlk:items/proc/tengu_tick
