function rlk:char/motion/cleanup
# 캐릭터 관련 플레이어 상태 초기화 (@s = 플레이어)
scoreboard players set @s skillCd 0
scoreboard players set @s burstCd 0
# 원소 에너지는 가득 찬 채로 시작(필요량보다 큰 값을 넣어 두면 char/tick 이 필요량으로 맞춤)
scoreboard players set @s energy 9999999
scoreboard players set @s energyPt 0
scoreboard players set @s skShown -1
scoreboard players set @s buShown -1
scoreboard players set @s enKey -1
scoreboard players set @s hurtLv 0
scoreboard players set @s starlight 0
scoreboard players set @s javQ 0
scoreboard players set @s javT 0
scoreboard players set @s javBonus 0
scoreboard players set @s lumP 0
scoreboard players set @s base_energyRecharge 100
execute unless score @s eqEnergyRecharge = @s eqEnergyRecharge run scoreboard players set @s eqEnergyRecharge 0
execute unless score @s energyRecharge matches 1.. run scoreboard players set @s energyRecharge 100
kill @e[tag=rlk_lstar]
kill @e[tag=rlk_jav]
# 활 · 요이미야
scoreboard players set @s bowT 0
scoreboard players set @s bowGap 0
scoreboard players set @s bowSeen 0
scoreboard players set @s bowUse 0
scoreboard players set @s bowRc 0
scoreboard players set @s bowCd 0
scoreboard players set @s bowQ -1
scoreboard players set @s bowF -1
scoreboard players set @s bowK 0
scoreboard players set @s bowSt 0
scoreboard players set @s bowPm -1
scoreboard players set #bowChg tmp 0
scoreboard players set @s yoiSk 0
scoreboard players set @s yoiPcCd 0
scoreboard players set @s yoiPcN 0
scoreboard players set @s yoiP 0
scoreboard players set @s yoiPT 0
scoreboard players set #yoiBoomCd tmp 0
scoreboard players reset 염초정화 stacks
scoreboard players reset 소매불 stacks
scoreboard players reset 염초화살 stacks
kill @e[tag=rlk_arrow]
# 스커크
scoreboard players set @s skM 0
scoreboard players set @s skDash 0
scoreboard players set @s skDep 0
scoreboard players set @s skDepB 0
scoreboard players set @s skDepCd 0
scoreboard players set @s skQ 0
scoreboard players set @s skBurst 0
scoreboard players set @s skPts 0
scoreboard players set #skMode tmp 0
scoreboard players set #skRiftCd tmp 0
attribute @s minecraft:movement_speed modifier remove rlk:skirk_dash
attribute @s minecraft:knockback_resistance modifier remove rlk:skirk
kill @e[tag=rlk_rift]
kill @e[tag=rlk_skb]
scoreboard players reset 일곱빛섬광 stacks
scoreboard players reset 고갈 stacks
scoreboard players reset 빠른이동 stacks
# 생명의 계약
scoreboard players set @s bol 0
scoreboard players reset 생명의계약 stacks
scoreboard players set @s naQ 0
# 클로린드
scoreboard players set @s clNV 0
scoreboard players set @s clLCd 0
scoreboard players set @s clBurst 0
scoreboard players set @s clP 0
scoreboard players set @s clPT 0
scoreboard players set #clShoot tmp 0
kill @e[tag=rlk_clb]
scoreboard players reset 밤순찰 stacks
# 아를레키노
scoreboard players set @s arM 0
scoreboard players reset 붉은가면 stacks
scoreboard players set @s bolKey -1
scoreboard players set @s fxT 0
scoreboard players set @s arSk 0
scoreboard players set @s stepT 0
# 전 캐릭터의 흔적 지우기: 사이드바 표시 · 적에게 남긴 표식 · 사라짐 효과 · 예약된 폭발
scoreboard players reset 차가운별빛 stacks
scoreboard players reset 예리한얼음 stacks
scoreboard players set @e[tag=rlk_mob] arDir 0
kill @e[tag=rlk_armk]
tag @e[tag=rlk_armd] remove rlk_armd
scoreboard players set @e[tag=rlk_mob] aurEnd 0
kill @e[tag=rlk_iq,scores={iqK=4}]
kill @e[tag=rlk_clm]
execute if entity @s[tag=rlk_body] run effect clear @s minecraft:invisibility
effect clear @e[tag=rlk_av,limit=1] minecraft:invisibility
scoreboard players set @s comboStep 0
# 캐릭터 변경: 이전 캐릭터의 평타 간격과 휘두르기 잠금(player/swing)을 바로 끝낸다
scoreboard players set @s atkCD 0
function rlk:player/swing/release
scoreboard players set @s fxId 0
attribute @s minecraft:movement_speed modifier remove rlk:bow_aim
scoreboard players set @s clPcCd 0
scoreboard players set @s clPcN 0
scoreboard players set @s clAuto 0
scoreboard players set @s clTg 0
# 원소폭발 시전 동작
function rlk:char/burst_wind_end
# 나비아
function rlk:char/navia/aim_end
kill @e[tag=rlk_nvgun]
scoreboard players set @s nvC 2
scoreboard players set @s nvCT 0
scoreboard players set @s nvCdE 0
scoreboard players set @s nvS 0
scoreboard players set @s nvST 0
scoreboard players set @s nvP 0
scoreboard players set @s nvQ 0
scoreboard players set @s nvQS 0
scoreboard players set @s nvFcd 0
scoreboard players set @s nvGun -1
scoreboard players set @s nvShot 0
scoreboard players set @s naQn 0
scoreboard players reset 결정파편 stacks
scoreboard players reset 결정축포 stacks
function rlk:char/navia/sh_clear
scoreboard players set @s nvShP 0
scoreboard players reset 결정축포 stacks
# 로노바 (불사의 저주 rnRev 는 판을 새로 시작할 때만 초기화)
scoreboard players set @s rnE1 0
scoreboard players set @s rnE2 0
scoreboard players set @s rnE3 0
scoreboard players set @s rnEn 0
scoreboard players set @s rnEcK -1
scoreboard players set @s rnFcd 0
scoreboard players set @s rnQ 0
kill @e[tag=rlk_rnec]
kill @e[tag=rlk_rnsh]
kill @e[tag=rlk_rnq]
kill @e[tag=rlk_rndm]
scoreboard players set @e[tag=rlk_mob] rnEr 0
scoreboard players set @e[tag=rlk_mob] aVoid 0
tag @e[tag=rlk_rndoom] remove rlk_rndoom
scoreboard players reset 잔향 stacks
scoreboard players reset 불사의저주 stacks
kill @e[tag=rlk_rncat]
execute if score @s rnDie matches 1.. run function rlk:char/ronova/die_end
scoreboard players set @s rnDie 0
kill @e[tag=rlk_hb_er]
# 네페르
scoreboard players set @s nfC 2
scoreboard players set @s nfCT 0
scoreboard players set @s nfCdE 0
scoreboard players set @s nfFcd 0
scoreboard players set @s nfSD 0
scoreboard players set @s nfPh 0
scoreboard players set @s nfPT 0
scoreboard players set @s nfQ 0
scoreboard players set @s nfDew 0
scoreboard players set @s nfDewW 0
scoreboard players set @s nfDewT 0
scoreboard players set @s nfVeil 0
scoreboard players set @s nfVeilT 0
scoreboard players set @s nfDwK -1
scoreboard players set #nfDecT tmp 0
function rlk:char/nefer/shadow_rm
kill @e[tag=rlk_nfsp]
kill @e[tag=rlk_nfq]
kill @e[tag=rlk_nfdw]
kill @e[tag=rlk_nfcat]
scoreboard players reset 풀이슬 stacks
scoreboard players reset 그림자춤 stacks
scoreboard players reset 기만의장막 stacks
