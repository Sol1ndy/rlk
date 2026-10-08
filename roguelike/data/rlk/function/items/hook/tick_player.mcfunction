# 플레이어별 매 틱 아이템 처리 (@s = 플레이어). 타이머/변신/스택 사이드바
# 가지고 있지 않은 아이템의 스택은 지운다(버리거나 판 직후 사이드바에 남지 않게)
execute unless score @s it_ice_quill matches 1.. run scoreboard players set #quillT itv 0
execute unless score @s it_source_samples matches 1.. run function rlk:items/proc/source_clear
execute unless score @s it_ember_oath matches 1.. run function rlk:items/proc/oath_clear
execute unless score @s it_salon_invite matches 1.. run scoreboard players set #fanT itv 0
execute unless score @s it_night_stars matches 1.. run function rlk:items/proc/night_clear
# 데모노미콘: 사이드바(스킬 4회 카운트) + 활성 마법 지속 발동
execute if score @s it_demonomicon matches 1.. run scoreboard players operation 데모노미콘 stacks = @s bookPages
execute if score @s it_demonomicon matches 1.. run scoreboard players display name 데모노미콘 stacks {text:"데모노미콘 페이지",color:"#C9A0FF"}
execute unless score @s it_demonomicon matches 1.. run scoreboard players reset 데모노미콘 stacks
execute if score @s it_demonomicon matches 1.. if score @s demonoBuff matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/demono_tick
# 금단의 도서: 페이지 #forbNeed(load 에서 설정)장 시 데모노미콘으로 진화 + 사이드바
execute if score @s it_forbidden_book matches 1.. if score @s forbPages >= #forbNeed tmp at @e[tag=rlk_body,limit=1] run function rlk:items/proc/forb_transform
execute if score @s it_forbidden_book matches 1.. run scoreboard players operation 마도서페이지 stacks = @s forbPages
execute if score @s it_forbidden_book matches 1.. run scoreboard players display name 마도서페이지 stacks {text:"금단의 도서 페이지",color:"#C9A0FF"}
execute unless score @s it_forbidden_book matches 1.. run scoreboard players reset 마도서페이지 stacks
# 키리온 변신 나선 이펙트
execute if score @s kirionFxT matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/kirion_fx_tick
execute if score @s kirionFxT matches 1.. run scoreboard players remove @s kirionFxT 1
# 봉인된 검: 킬수 사이드바 (보유 시만 표시)
execute if score @s it_sealed_sword matches 1.. run scoreboard players operation 봉인검킬수 stacks = @s kirionKills
execute if score @s it_sealed_sword matches 1.. run scoreboard players display name 봉인검킬수 stacks {text:"봉인된 검 킬 수",color:"#FF8A5A"}
execute unless score @s it_sealed_sword matches 1.. run scoreboard players reset 봉인검킬수 stacks
# 고통 & 절망: 스택 유지시간
execute if score @s pdT matches 1.. run scoreboard players remove @s pdT 1
execute if score @s pdT matches 0 run scoreboard players set @s pdStack 0
# 초월 · 악요개안: 협동 공격 쿨타임 + 어깨 뒤에 떠 있는 눈
execute if score @s eyeCd matches 1.. run scoreboard players remove @s eyeCd 1
execute if score @s it_stormy_eye matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/eye_follow
execute unless score @s it_stormy_eye matches 1.. if entity @e[tag=rlk_eye,limit=1] run kill @e[tag=rlk_eye]
# 페보니우스 비전 쿨타임
execute if score @s favCd matches 1.. run scoreboard players remove @s favCd 1
# 아이템 타이머 / 까마귀 / 얼음 깃 표시
execute if score #rainT itv matches 1.. run scoreboard players remove #rainT itv 1
execute if score #rainCd itv matches 1.. run scoreboard players remove #rainCd itv 1
execute if score #flagIn itv matches 1.. run scoreboard players remove #flagIn itv 1
execute if score #mapleT itv matches 1.. run scoreboard players remove #mapleT itv 1
execute if score #mapleCd itv matches 1.. run scoreboard players remove #mapleCd itv 1
execute if score #quillT itv matches 1.. run scoreboard players remove #quillT itv 1
execute if score #bunnyCd itv matches 1.. run scoreboard players remove #bunnyCd itv 1
execute if score #talCd itv matches 1.. run scoreboard players remove #talCd itv 1
execute if score #thiefCd itv matches 1.. run scoreboard players remove #thiefCd itv 1
execute if score #blossomCd itv matches 1.. run scoreboard players remove #blossomCd itv 1
execute if score #ravenT itv matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/raven_tick
execute if score #ravenT itv matches 1.. run scoreboard players remove #ravenT itv 1
execute unless score #quillT itv matches 1.. run scoreboard players set #quill itv 0
execute if score #quill itv matches 1.. run scoreboard players operation 얼음깃 stacks = #quill itv
execute if score #quill itv matches 1.. run scoreboard players display name 얼음깃 stacks {text:"얼음 깃",color:"#9FE8F5"}
execute unless score #quill itv matches 1.. run scoreboard players reset 얼음깃 stacks
# 아이템 타이머(2차) / 몸을 따라다니는 효과 / 사이드바
execute if score #ringT itv matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/ring_tick
execute if score #gringT itv matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/gring_tick
execute if score #salonT itv matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/salon_tick
execute if score #ringT itv matches 1.. run scoreboard players remove #ringT itv 1
execute if score #gringT itv matches 1.. run scoreboard players remove #gringT itv 1
execute if score #salonT itv matches 1.. run scoreboard players remove #salonT itv 1
execute if score #gflagIn itv matches 1.. run scoreboard players remove #gflagIn itv 1
execute if score #wispCd itv matches 1.. run scoreboard players remove #wispCd itv 1
execute if score #muskT itv matches 1.. run scoreboard players remove #muskT itv 1
execute if score #skCd itv matches 1.. run scoreboard players remove #skCd itv 1
execute if score #oathT itv matches 1.. run scoreboard players remove #oathT itv 1
execute if score #src1 itv matches 1.. run scoreboard players remove #src1 itv 1
execute if score #src2 itv matches 1.. run scoreboard players remove #src2 itv 1
execute if score #src3 itv matches 1.. run scoreboard players remove #src3 itv 1
execute if score #src4 itv matches 1.. run scoreboard players remove #src4 itv 1
execute if score #src5 itv matches 1.. run scoreboard players remove #src5 itv 1
execute if score #src6 itv matches 1.. run scoreboard players remove #src6 itv 1
execute if score #src7 itv matches 1.. run scoreboard players remove #src7 itv 1
scoreboard players set #srcN itv 0
execute if score #src1 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src2 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src3 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src4 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src5 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src6 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src7 itv matches 1.. run scoreboard players add #srcN itv 1
# 생명줄: 대쉬가 끝났으면 실이 감긴 적에게 피해
execute if entity @e[tag=rlk_llm,limit=1] unless score @s dashMoveT matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/lifeline_fire
execute if score #srcN itv matches 1.. run scoreboard players operation 음원 stacks = #srcN itv
execute if score #srcN itv matches 1.. run scoreboard players display name 음원 stacks {text:"켜진 음원",color:"#A5D94A"}
execute unless score #srcN itv matches 1.. run scoreboard players reset 음원 stacks
execute if score #oath itv matches 1.. run scoreboard players operation 전의 stacks = #oath itv
execute if score #oath itv matches 1.. run scoreboard players display name 전의 stacks {text:"전의",color:"#FF6B4A"}
execute unless score #oath itv matches 1.. run scoreboard players reset 전의 stacks
# 아이템(3차): 열기 / 무결점 보호막 / 지니 램프 / 잠결의 별 / 타이머
execute if score #fanT itv matches 1.. run function rlk:items/proc/fan_tick
execute unless score #fanT itv matches 1.. run scoreboard players set #fan itv 0
scoreboard players operation #t1 itv = #seamT itv
scoreboard players operation #t1 itv %= #st50 tmp
execute if score #seamT itv matches 1.. if score #t1 itv matches 1 run function rlk:items/proc/seam_pulse
scoreboard players operation #t1 itv = #genieT itv
scoreboard players operation #t1 itv %= #st40 tmp
execute if score #genieT itv matches 1.. if score #t1 itv matches 1 run function rlk:items/proc/genie_pulse
execute if score #nightT itv matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/night_tick
execute if score #jadeT itv matches 1.. run scoreboard players remove #jadeT itv 1
execute if score #mayaT itv matches 1.. run scoreboard players remove #mayaT itv 1
execute if score #fanT itv matches 1.. run scoreboard players remove #fanT itv 1
execute if score #seamT itv matches 1.. run scoreboard players remove #seamT itv 1
execute if score #dragT itv matches 1.. run scoreboard players remove #dragT itv 1
execute if score #tenguT itv matches 1.. run scoreboard players remove #tenguT itv 1
execute if score #operaT itv matches 1.. run scoreboard players remove #operaT itv 1
execute if score #barCd itv matches 1.. run scoreboard players remove #barCd itv 1
execute if score #nightT itv matches 1.. run scoreboard players remove #nightT itv 1
execute if score #genieT itv matches 1.. run scoreboard players remove #genieT itv 1
execute if score #kinT itv matches 1.. run scoreboard players remove #kinT itv 1
execute if score #orbCd itv matches 1.. run scoreboard players remove #orbCd itv 1
execute if score #slimeT itv matches 1.. run scoreboard players remove #slimeT itv 1
execute if score #fan itv matches 1.. run scoreboard players operation 열기 stacks = #fan itv
execute if score #fan itv matches 1.. run scoreboard players display name 열기 stacks {text:"열기",color:"#4FB8FF"}
execute unless score #fan itv matches 1.. run scoreboard players reset 열기 stacks
execute if score #stars itv matches 1.. run scoreboard players operation 잠결의별 stacks = #stars itv
execute if score #stars itv matches 1.. run scoreboard players display name 잠결의별 stacks {text:"잠결의 별",color:"#9FE8F5"}
execute unless score #stars itv matches 1.. run scoreboard players reset 잠결의별 stacks
# 고통 & 절망: 스택 사이드바
execute unless score @s it_pain_despair matches 1.. run scoreboard players set @s pdStack 0
execute unless score @s it_pain_despair matches 1.. run scoreboard players set @s pdT 0
execute if score @s pdStack matches 1.. run scoreboard players operation 고통절망 stacks = @s pdStack
execute if score @s pdStack matches 1.. run scoreboard players display name 고통절망 stacks {text:"고통 & 절망",color:"#D94F6B"}
execute unless score @s pdStack matches 1.. run scoreboard players reset 고통절망 stacks
# 아이템(4차): 타이머 / 다음 틱에 발동하는 효과 / 주기 회복 / 사이드바
execute if score #sinT itv matches 1.. run scoreboard players remove #sinT itv 1
execute if score #candT itv matches 1.. run scoreboard players remove #candT itv 1
execute if score #craneT itv matches 1.. run scoreboard players remove #craneT itv 1
execute if score #maidCd itv matches 1.. run scoreboard players remove #maidCd itv 1
execute if score #pillowT itv matches 1.. run scoreboard players remove #pillowT itv 1
execute if score #loomT itv matches 1.. run scoreboard players remove #loomT itv 1
execute if score #mechCd itv matches 1.. run scoreboard players remove #mechCd itv 1
execute if score #lionCd itv matches 1.. run scoreboard players remove #lionCd itv 1
execute if score #lilyT itv matches 1.. run scoreboard players remove #lilyT itv 1
execute if score #lilyCd itv matches 1.. run scoreboard players remove #lilyCd itv 1
execute if score #harmT itv matches 1.. run scoreboard players remove #harmT itv 1
execute if score #dandT itv matches 1.. run scoreboard players remove #dandT itv 1
execute if score #harmT itv matches ..0 run scoreboard players set #harmN itv 0
execute if score #craneQ itv matches 1 run scoreboard players set #craneQ itv 2
execute if score #craneQ itv matches 2 at @e[tag=rlk_body,limit=1] run function rlk:items/proc/crane_go
execute if score #lilyHit itv matches 1 at @e[tag=rlk_body,limit=1] run function rlk:items/proc/lily_boom
execute if score #lionQ itv matches 1 at @e[tag=rlk_body,limit=1] run function rlk:items/proc/lion_boom
execute if score #nurseQ itv matches 1 run function rlk:items/proc/nurse_pay
execute if score @s it_life_gourd matches 1.. run function rlk:items/proc/gourd_tick
execute if score #harmN itv matches 1.. run scoreboard players operation 공상의악보 stacks = #harmN itv
execute if score #harmN itv matches 1.. run scoreboard players display name 공상의악보 stacks {text:"공상의 악보",color:"#E0526A"}
execute unless score #harmN itv matches 1.. run scoreboard players reset 공상의악보 stacks
scoreboard players operation #lilyS itv = #lilyT itv
scoreboard players add #lilyS itv 19
scoreboard players operation #lilyS itv /= #st20 tmp
execute if score #lilyS itv matches 1.. run scoreboard players operation 수련의무희 stacks = #lilyS itv
execute if score #lilyS itv matches 1.. run scoreboard players display name 수련의무희 stacks {text:"수련의 무희",color:"#4FB8FF"}
execute unless score #lilyS itv matches 1.. run scoreboard players reset 수련의무희 stacks
# 서리달의 은잔: 중력의 물결 · 중력 쿨 · 월광(달 피해 보너스)
execute if score #cgRipT itv matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/cg_rip_tick
execute if score #cgRipT itv matches 1.. run scoreboard players remove #cgRipT itv 1
execute if score #cgRipT itv matches 0 run function rlk:items/proc/cg_rip_end
execute if score #cgC1 itv matches 1.. run scoreboard players remove #cgC1 itv 1
execute if score #cgC2 itv matches 1.. run scoreboard players remove #cgC2 itv 1
execute if score #cgC3 itv matches 1.. run scoreboard players remove #cgC3 itv 1
scoreboard players set #lnBuff itv 0
execute if score #cgMoonT itv matches 1.. run scoreboard players operation #lnBuff itv = #cgMoon tmp
execute if score #cgMoonT itv matches 1.. run scoreboard players remove #cgMoonT itv 1
execute if score #cgMoonT itv matches 1.. at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.85,0.88,1.0],scale:0.7} ~ ~2.2 ~ 0.3 0.1 0.3 0 1
# 각인 만월 2개: 달 반응 피해
execute if score fullmoon engN matches 2.. run scoreboard players operation #lnBuff itv += #fmDmg tmp
