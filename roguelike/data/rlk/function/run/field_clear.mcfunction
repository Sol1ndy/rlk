execute as @a[tag=player] run function rlk:char/motion/stop
# 필드에 남은 것을 모두 지운다 (떨어진 아이템·골드·사파이어는 부르는 쪽에서 먼저 처리)
kill @e[tag=rlk_page_orb]
kill @e[tag=rlk_healorb]
kill @e[tag=rlk_core]
kill @e[tag=rlk_crystal]
kill @e[tag=rlk_epart]
kill @e[tag=rlk_lstar]
kill @e[tag=rlk_jav]
kill @e[tag=rlk_arrow]
kill @e[tag=rlk_rift]
kill @e[tag=rlk_skb]
kill @e[tag=rlk_clb]
kill @e[tag=rlk_clm]
kill @e[tag=rlk_kslash]
kill @e[tag=rlk_eyeq]
kill @e[tag=rlk_dashmk]
kill @e[tag=dmgText]
kill @e[tag=rlk_raven]
kill @e[tag=rlk_pot]
kill @e[tag=rlk_flag]
kill @e[tag=rlk_quillq]
kill @e[tag=rlk_decoy]
kill @e[tag=rlk_decoym]
kill @e[tag=rlk_blossom]
kill @e[tag=rlk_blq]
kill @e[tag=rlk_iq]
kill @e[tag=rlk_jelly]
kill @e[tag=rlk_gflag]
kill @e[tag=rlk_doll]
kill @e[tag=rlk_wisp]
kill @e[tag=rlk_hound]
kill @e[tag=rlk_vortex]
kill @e[tag=rlk_sakura]
kill @e[tag=rlk_storm]
kill @e[tag=rlk_meteor]
kill @e[tag=rlk_case]
kill @e[tag=rlk_tengu]
kill @e[type=minecraft:experience_orb]
tag @e[tag=rlk_llm] remove rlk_llm
# 따라다니던 효과의 남은 시간도 끝낸다(까마귀·고리·살롱 멤버 등)
scoreboard players set #ravenT itv 0
scoreboard players set #rainT itv 0
scoreboard players set #flagIn itv 0
scoreboard players set #ringT itv 0
scoreboard players set #gringT itv 0
scoreboard players set #salonT itv 0
scoreboard players set #gflagIn itv 0
scoreboard players set #nightT itv 0
scoreboard players set #seamT itv 0
scoreboard players set #genieT itv 0
scoreboard players set #jadeT itv 0
kill @e[tag=rlk_lndrift]
kill @e[tag=rlk_dcore]
kill @e[tag=rlk_coreP]
kill @e[tag=rlk_rnsh]
kill @e[tag=rlk_salonP]
kill @e[tag=rlk_salon]
kill @e[tag=rlk_salonPv]
