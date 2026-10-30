function rlk:boss/raiden/uninstall
kill @e[tag=rlk_raiden]
# 중간보스: 전투 정리 · 보스바 · 점수 · 경기장 청크 고정 해제
function rlk:mboss/uninstall
# rift (build_rift.py)
function rlk:room/rift/uninstall
scoreboard objectives remove lcSeen
execute as @a[tag=player] run function rlk:char/motion/stop
# 시스템 제거: 임시 엔티티/UI 아이템/스코어보드 정리 후 틱 처리 정지 (사용: /function rlk:uninstall)
kill @e[tag=rlk_plkb]
kill @e[tag=rlk_plkb_source]
scoreboard objectives remove pkbT
effect clear @a[tag=player] minecraft:night_vision
kill @e[tag=rlk_melee_origin]
execute as @a[tag=player,scores={vMap=1}] run function rlk:view/map_close
kill @e[tag=rlk_mapreturn]
kill @e[tag=rlk_mapv]
data remove storage rlk:map ret
kill @e[tag=dmgText]
kill @e[type=minecraft:interaction,tag=atkBlock]
kill @e[type=minecraft:interaction,tag=atkStrike]
kill @e[tag=rlk_mshield]
kill @e[tag=rlk_hb_bg]
kill @e[tag=rlk_hb_fg]
kill @e[tag=rlk_hb_num]
kill @e[tag=rlk_hb_lv]
kill @e[tag=rlk_hb_icon]
kill @e[tag=rlk_frz_ice]
kill @e[tag=rlk_ditem]
kill @e[tag=rlk_dinfo]
kill @e[tag=rlk_dbtn]
kill @e[tag=rlk_dlbl]
kill @e[tag=rlk_healorb]
kill @e[tag=rlk_gold]
kill @e[tag=rlk_shfx]
kill @e[tag=rlk_storm]
kill @e[tag=rlk_meteor]
kill @e[tag=rlk_case]
kill @e[tag=rlk_tengu]
kill @e[tag=rlk_iq]
kill @e[tag=rlk_jelly]
kill @e[tag=rlk_gflag]
kill @e[tag=rlk_doll]
kill @e[tag=rlk_wisp]
kill @e[tag=rlk_hound]
kill @e[tag=rlk_vortex]
kill @e[tag=rlk_sakura]
kill @e[tag=rlk_raven]
kill @e[tag=rlk_pot]
kill @e[tag=rlk_flag]
kill @e[tag=rlk_quillq]
kill @e[tag=rlk_decoy]
kill @e[tag=rlk_decoym]
kill @e[tag=rlk_blossom]
kill @e[tag=rlk_blq]
kill @e[tag=rlk_epart]
kill @e[tag=rlk_pk]
execute as @a[tag=player] if entity @e[tag=rlk_view,limit=1] run function rlk:view/teardown
kill @e[tag=rlk_view]
tag @a remove rlk_body
team remove rlk_cam
team remove rlk_stun
data remove storage rlk:view cam
execute in minecraft:overworld run forceload remove 104 4
kill @e[tag=rlk_eye]
kill @e[tag=rlk_eyeq]
kill @e[tag=rlk_lstar]
kill @e[tag=rlk_jav]
kill @e[tag=rlk_arrow]
kill @e[tag=rlk_rift]
kill @e[tag=rlk_skb]
kill @e[tag=rlk_clb]
kill @e[tag=rlk_clm]
clear @a *[minecraft:custom_data~{rlk_char:1b}]
# 방 시스템: 진행 중인 런 정리(던전 구역 블록은 남음 — 지우려면 제거 전에 /function rlk:room/remove)
execute if score #active room matches 1 as @a[tag=player,limit=1] run function rlk:run/stop
kill @e[tag=rlk_room]
kill @e[tag=rlk_cmglob]
kill @e[tag=rlk_cmlink]
kill @e[tag=rlk_cmp]
tag @a remove rlk_setup
clear @a minecraft:filled_map[minecraft:custom_data~{rlk_map:1b}]
execute as @a run attribute @s minecraft:movement_speed modifier remove rlk:frozen
execute as @a run attribute @s minecraft:jump_strength modifier remove rlk:frozen
# 휘두르기: 지금 판은 점프 힘 수정자만 쓴다. 이동 속도 수정자는 D12 판에서 남았을 수 있는 것(player/swing/legacy)
execute as @a run attribute @s minecraft:movement_speed modifier remove rlk:swing_hold
execute as @a run attribute @s minecraft:jump_strength modifier remove rlk:swing_hold
tag @a remove rlk_sw13
kill @e[tag=rlk_shop_item]
kill @e[tag=rlk_shop_info]
kill @e[tag=rlk_shop_lbl]
kill @e[tag=rlk_shop_btn]
kill @e[tag=rlk_shop_reroll]
kill @e[tag=rlk_shop_rlbl]
function rlk:items/hook/reset_world
tag @e remove rlk_mob
clear @a *[minecraft:custom_data~{rlk_stat:1b}]
clear @a *[minecraft:custom_data~{rlk_eng:1b}]
clear @a *[minecraft:custom_data~{rlk_engi:1b}]
clear @a *[minecraft:custom_data~{rlk_invd:1b}]
clear @a *[minecraft:custom_data~{rlk_lock:1b}]
clear @a *[minecraft:custom_data~{rlk_ui:{}}]
clear @a *[minecraft:custom_data~{rlk:{}}]
# 아이템 보유 플래그(it_<id>) 제거
data modify storage rlk:items fscan set from storage rlk:items ids
function rlk:items/unreg_flags_loop
# 속성 원복
execute as @a run attribute @s minecraft:max_health base set 20
execute as @a run attribute @s minecraft:movement_speed base set 0.1
execute as @a run attribute @s minecraft:attack_speed base set 4
execute as @a run attribute @s minecraft:attack_damage base set 1
experience set @a 0 levels
experience set @a 0 points
scoreboard objectives remove aEl
scoreboard objectives remove aFire
scoreboard objectives remove aGrass
scoreboard objectives remove aIcd
scoreboard objectives remove aIce
scoreboard objectives remove aKind
scoreboard objectives remove aLife
scoreboard objectives remove aSub
scoreboard objectives remove aThunder
scoreboard objectives remove aVoid
scoreboard objectives remove aWater
scoreboard objectives remove aimingDrop
scoreboard objectives remove ampAtk
scoreboard objectives remove anemoBonus
scoreboard objectives remove arDir
scoreboard objectives remove arM
scoreboard objectives remove arSk
scoreboard objectives remove armY
scoreboard objectives remove armZ
scoreboard objectives remove atk
scoreboard objectives remove atkCD
scoreboard objectives remove atkFlat
scoreboard objectives remove atkPct
scoreboard objectives remove atkSpeed
scoreboard objectives remove aurEnd
scoreboard objectives remove avId
scoreboard objectives remove base_atk
scoreboard objectives remove base_atkSpeed
scoreboard objectives remove base_critChance
scoreboard objectives remove base_critDamage
scoreboard objectives remove base_def
scoreboard objectives remove base_elemMastery
scoreboard objectives remove base_energyRecharge
scoreboard objectives remove base_maxHealth
scoreboard objectives remove base_moveSpeed
scoreboard objectives remove berT
scoreboard objectives remove bol
scoreboard objectives remove bolKey
scoreboard objectives remove bookPages
scoreboard objectives remove bowCd
scoreboard objectives remove bowF
scoreboard objectives remove bowGap
scoreboard objectives remove bowK
scoreboard objectives remove bowPm
scoreboard objectives remove bowQ
scoreboard objectives remove bowQc
scoreboard objectives remove bowQo
scoreboard objectives remove bowRc
scoreboard objectives remove bowSeen
scoreboard objectives remove bowSt
scoreboard objectives remove bowT
scoreboard objectives remove bowUse
scoreboard objectives remove buShown
scoreboard objectives remove buT
scoreboard objectives remove burnDmg
scoreboard objectives remove burnI
scoreboard objectives remove burnOn
scoreboard objectives remove burstCd
scoreboard objectives remove cF
scoreboard objectives remove cX0
scoreboard objectives remove cX1
scoreboard objectives remove cY0
scoreboard objectives remove cY1
scoreboard objectives remove cZ0
scoreboard objectives remove cZ1
scoreboard objectives remove cboIdle
scoreboard objectives remove clAuto
scoreboard objectives remove clBurst
scoreboard objectives remove clLCd
scoreboard objectives remove clNV
scoreboard objectives remove clP
scoreboard objectives remove clPT
scoreboard objectives remove clPcCd
scoreboard objectives remove clPcN
scoreboard objectives remove clTg
scoreboard objectives remove cmCd
scoreboard objectives remove cmCd2
scoreboard objectives remove cmD
scoreboard objectives remove cmD2
scoreboard objectives remove cmEl
scoreboard objectives remove cmF
scoreboard objectives remove cmId
scoreboard objectives remove cmLv
scoreboard objectives remove cmN
scoreboard objectives remove cmPx
scoreboard objectives remove cmPy
scoreboard objectives remove cmPz
scoreboard objectives remove cmS
scoreboard objectives remove cmSh
scoreboard objectives remove cmShM
scoreboard objectives remove cmT
scoreboard objectives remove cmV
scoreboard objectives remove cmVx
scoreboard objectives remove cmVy
scoreboard objectives remove cmVz
scoreboard objectives remove cmYaw
scoreboard objectives remove comboStep
scoreboard objectives remove critChance
scoreboard objectives remove critDamage
scoreboard objectives remove cryoBonus
scoreboard objectives remove curHealth
scoreboard objectives remove cxMode
scoreboard objectives remove cxPage
scoreboard objectives remove cxTab
scoreboard objectives remove dFire
scoreboard objectives remove dGrass
scoreboard objectives remove dIce
scoreboard objectives remove dThunder
scoreboard objectives remove dVoid
scoreboard objectives remove dWater
scoreboard objectives remove da
scoreboard objectives remove dashCharge
scoreboard objectives remove dashCool
scoreboard objectives remove dashDX
scoreboard objectives remove dashDZ
scoreboard objectives remove dashInvT
scoreboard objectives remove dashMoveT
scoreboard objectives remove dashPX
scoreboard objectives remove dashPZ
scoreboard objectives remove dashRegen
scoreboard objectives remove dashUX
scoreboard objectives remove dashUZ
scoreboard objectives remove dashUpN
scoreboard objectives remove db
scoreboard objectives remove dbgDropI
scoreboard objectives remove dbgPage
scoreboard objectives remove dbgPageCur
scoreboard objectives remove dead
scoreboard objectives remove def
scoreboard objectives remove defFlat
scoreboard objectives remove defPct
scoreboard objectives remove demonoBuff
scoreboard objectives remove demonoType
scoreboard objectives remove dendroBonus
scoreboard objectives remove devMode
scoreboard objectives remove dgid
scoreboard objectives remove dopenT
scoreboard objectives remove dprice
scoreboard objectives remove dst
scoreboard objectives remove dvis
scoreboard objectives remove ecDmg
scoreboard objectives remove ecI
scoreboard objectives remove elAct
scoreboard objectives remove electroBonus
scoreboard objectives remove elemMastery
scoreboard objectives remove enKey
scoreboard objectives remove energy
scoreboard objectives remove energyPt
scoreboard objectives remove energyRecharge
scoreboard objectives remove eng
scoreboard objectives remove engAdd
scoreboard objectives remove engCur
scoreboard objectives remove engDev
scoreboard objectives remove engItems
scoreboard objectives remove engN
scoreboard objectives remove engSub
scoreboard objectives remove eqAnemoBonus
scoreboard objectives remove eqAtkFlat
scoreboard objectives remove eqAtkPct
scoreboard objectives remove eqAtkSpeed
scoreboard objectives remove eqCritChance
scoreboard objectives remove eqCritDamage
scoreboard objectives remove eqCryoBonus
scoreboard objectives remove eqDefFlat
scoreboard objectives remove eqDefPct
scoreboard objectives remove eqDendroBonus
scoreboard objectives remove eqElectroBonus
scoreboard objectives remove eqElemMastery
scoreboard objectives remove eqEnergyRecharge
scoreboard objectives remove eqGeoBonus
scoreboard objectives remove eqHpFlat
scoreboard objectives remove eqHpPct
scoreboard objectives remove eqHydroBonus
scoreboard objectives remove eqMoveSpeed
scoreboard objectives remove eqPhysBonus
scoreboard objectives remove eqPyroBonus
scoreboard objectives remove erodeEnd
scoreboard objectives remove ex0
scoreboard objectives remove ex1
scoreboard objectives remove eyeAnim
scoreboard objectives remove eyeCd
scoreboard objectives remove ez0
scoreboard objectives remove ez1
scoreboard objectives remove favAt
scoreboard objectives remove favCd
scoreboard objectives remove fbMark
scoreboard objectives remove forbPages
scoreboard objectives remove frzT
scoreboard objectives remove fxId
scoreboard objectives remove fxT
scoreboard objectives remove gCd
scoreboard objectives remove gShield
scoreboard objectives remove geoBonus
scoreboard objectives remove gold
scoreboard objectives remove gval
scoreboard objectives remove hpFlat
scoreboard objectives remove hpKey
scoreboard objectives remove hpMaxPrev
scoreboard objectives remove hpPct
scoreboard objectives remove hudHold
scoreboard objectives remove hudKey
scoreboard objectives remove hurtElem
scoreboard objectives remove hurtLv
scoreboard objectives remove hydroBonus
scoreboard objectives remove icKey
scoreboard objectives remove icdC
scoreboard objectives remove icdT
scoreboard objectives remove infuse
scoreboard objectives remove infuseT
scoreboard objectives remove init
scoreboard objectives remove intOwner
scoreboard objectives remove invCnt
scoreboard objectives remove invDirty
scoreboard objectives remove invCap
scoreboard objectives remove invEvt
scoreboard objectives remove iqK
scoreboard objectives remove itv
scoreboard objectives remove javBonus
scoreboard objectives remove javN
scoreboard objectives remove javQ
scoreboard objectives remove javT
scoreboard objectives remove jcrit
scoreboard objectives remove jdmg
scoreboard objectives remove keenCd
scoreboard objectives remove keenNext
scoreboard objectives remove kirionFxT
scoreboard objectives remove kirionKills
scoreboard objectives remove lact
scoreboard objectives remove level
scoreboard objectives remove lgid
scoreboard objectives remove life
scoreboard objectives remove lnBloom
scoreboard objectives remove lnCr
scoreboard objectives remove lnEC
scoreboard objectives remove lnI
scoreboard objectives remove lob
scoreboard objectives remove lobRoom
scoreboard objectives remove lumP
scoreboard objectives remove manageTick
scoreboard objectives remove maxHealth
scoreboard objectives remove mhp0
scoreboard objectives remove mhpC
scoreboard objectives remove mhpM
scoreboard objectives remove mirEnd
scoreboard objectives remove mlv
scoreboard objectives remove moveSpeed
scoreboard objectives remove msid
scoreboard objectives remove naQ
scoreboard objectives remove naQc
scoreboard objectives remove naQn
scoreboard objectives remove nfC
scoreboard objectives remove nfCT
scoreboard objectives remove nfCdE
scoreboard objectives remove nfDew
scoreboard objectives remove nfDewT
scoreboard objectives remove nfDewW
scoreboard objectives remove nfDwI
scoreboard objectives remove nfDwK
scoreboard objectives remove nfDwP
scoreboard objectives remove nfFcd
scoreboard objectives remove nfPT
scoreboard objectives remove nfPh
scoreboard objectives remove nfQ
scoreboard objectives remove nfQV
scoreboard objectives remove nfSD
scoreboard objectives remove nfVeil
scoreboard objectives remove nfVeilT
scoreboard objectives remove nvA
scoreboard objectives remove nvC
scoreboard objectives remove nvCT
scoreboard objectives remove nvCdE
scoreboard objectives remove nvFcd
scoreboard objectives remove nvGap
scoreboard objectives remove nvGun
scoreboard objectives remove nvShot
scoreboard objectives remove nvHit
scoreboard objectives remove nvP
scoreboard objectives remove nvQ
scoreboard objectives remove nvQS
scoreboard objectives remove nvQT
scoreboard objectives remove nvS
scoreboard objectives remove nvST
scoreboard objectives remove nvShI
scoreboard objectives remove nvShK
scoreboard objectives remove nvShP
scoreboard objectives remove oact
scoreboard objectives remove oarg
scoreboard objectives remove ogid
scoreboard objectives remove omenEnd
scoreboard objectives remove pcVal
scoreboard objectives remove pdStack
scoreboard objectives remove pdT
scoreboard objectives remove physBonus
scoreboard objectives remove pid
scoreboard objectives remove pkCd
scoreboard objectives remove pkConf
scoreboard objectives remove pkHI
scoreboard objectives remove pkHK
scoreboard objectives remove pkIdx
scoreboard objectives remove pkKind
scoreboard objectives remove pkMode
scoreboard objectives remove pkPending
scoreboard objectives remove pkRedraw
scoreboard objectives remove pkRr
scoreboard objectives remove pkSel
scoreboard objectives remove pkSubT
scoreboard objectives remove pkSwap
scoreboard objectives remove pyroBonus
scoreboard objectives remove quickT
scoreboard objectives remove rcT
scoreboard objectives remove rcU
scoreboard objectives remove rnDie
scoreboard objectives remove rnE1
scoreboard objectives remove rnE2
scoreboard objectives remove rnE3
scoreboard objectives remove rnEcI
scoreboard objectives remove rnEcK
scoreboard objectives remove rnEcd
scoreboard objectives remove rnEn
scoreboard objectives remove rnEr
scoreboard objectives remove rnErT
scoreboard objectives remove rnFcd
scoreboard objectives remove rnId
scoreboard objectives remove rnNoE
scoreboard objectives remove rnQ
scoreboard objectives remove rnRev
scoreboard objectives remove rnTg
scoreboard objectives remove room
scoreboard objectives remove rxDmg
scoreboard objectives remove rxDmg3
scoreboard objectives remove rxEl
scoreboard objectives remove rxQ
scoreboard objectives remove sT
scoreboard objectives remove sapphire
scoreboard objectives remove dice
scoreboard objectives remove nodeHp
scoreboard objectives remove enhL
scoreboard objectives remove scT
scoreboard objectives remove scanTick
scoreboard objectives remove sdelay
scoreboard objectives remove shieldEl
scoreboard objectives remove shieldHP
scoreboard objectives remove shieldT
scoreboard objectives remove shopGid
scoreboard objectives remove shopOpenT
scoreboard objectives remove sidx
scoreboard objectives remove skBurst
scoreboard objectives remove skDash
scoreboard objectives remove skDep
scoreboard objectives remove skDepB
scoreboard objectives remove skDepCd
scoreboard objectives remove skEnd
scoreboard objectives remove skM
scoreboard objectives remove skPts
scoreboard objectives remove skQ
scoreboard objectives remove skShown
scoreboard objectives remove skillCd
scoreboard objectives remove smI
scoreboard objectives remove sph
scoreboard objectives remove stacks
scoreboard objectives remove starlight
scoreboard objectives remove stepT
scoreboard objectives remove stunT
scoreboard objectives remove swCut
scoreboard objectives remove swHold
scoreboard objectives remove swJump
scoreboard objectives remove swungAt
scoreboard objectives remove talEnd
scoreboard objectives remove tmp
scoreboard objectives remove ttlT
scoreboard objectives remove uiCd
scoreboard objectives remove uiHash
scoreboard objectives remove vAimT
scoreboard objectives remove vBig
scoreboard objectives remove vDp
scoreboard objectives remove vDy
scoreboard objectives remove vMap
scoreboard objectives remove vMapH
scoreboard objectives remove vMapT
scoreboard objectives remove vPitch
scoreboard objectives remove vSnk
scoreboard objectives remove vTtp
scoreboard objectives remove vYaw
scoreboard objectives remove vhp
scoreboard objectives remove view
scoreboard objectives remove wr
scoreboard objectives remove wx
scoreboard objectives remove wz
scoreboard objectives remove xp
scoreboard objectives remove xpDrop
scoreboard objectives remove xpLeft
scoreboard objectives remove xpNeed
scoreboard objectives remove xpPulse
scoreboard objectives remove yoiP
scoreboard objectives remove yoiPT
scoreboard objectives remove yoiPcCd
scoreboard objectives remove yoiPcN
scoreboard objectives remove yoiSk
scoreboard objectives remove zid
scoreboard objectives remove zkind
scoreboard objectives remove zst
scoreboard objectives remove stage
data modify storage rlk:config installed set value 0b
tellraw @a {"text":"[로그라이크] 시스템이 제거되었습니다. (/reload 하면 다시 설치됩니다. 완전히 끄려면 데이터팩을 비활성화하세요)","color":"red"}
kill @e[tag=rlk_lobby]
forceload remove 80 14 134 64

scoreboard objectives remove snd

scoreboard objectives remove vMapL
scoreboard objectives remove vMapR

scoreboard objectives remove cmAF
scoreboard objectives remove cmAH
scoreboard objectives remove cmAR
scoreboard objectives remove cmAX
scoreboard objectives remove cmAZ
scoreboard objectives remove cmAP
scoreboard objectives remove cmAD
function rlk:cm/c2/uninstall
function rlk:cm/c3/uninstall

scoreboard objectives remove pmAtkPending
scoreboard objectives remove pmAtkStep
scoreboard objectives remove pmAtkKind
scoreboard objectives remove pmStrike
scoreboard objectives remove pmSecond
scoreboard objectives remove pmThird
scoreboard objectives remove pmChain
scoreboard objectives remove pmMoveLock
scoreboard objectives remove pmLockUntil
scoreboard objectives remove pmActive
scoreboard objectives remove pmTick
scoreboard objectives remove pmLen
scoreboard objectives remove pmChar
scoreboard objectives remove pmSpeed
scoreboard objectives remove pmAcc
scoreboard objectives remove pmStep
data remove storage rlk:player_motion active

scoreboard objectives remove pmVisible
scoreboard objectives remove pmRigChar
scoreboard objectives remove pmLocMode
scoreboard objectives remove pmWantMode
scoreboard objectives remove pmLocT
scoreboard objectives remove pmLocAcc
scoreboard objectives remove pmLocSpeed
scoreboard objectives remove pmBlend
scoreboard objectives remove pmPX
scoreboard objectives remove pmPZ
scoreboard objectives remove pmPosValid
scoreboard objectives remove pmWeapon
scoreboard objectives remove pmWantW
scoreboard objectives remove pmSheath
scoreboard objectives remove pmShT
scoreboard objectives remove pmLocS
scoreboard objectives remove pmShFx
scoreboard objectives remove pmWAt
scoreboard objectives remove pmWModel
data remove storage rlk:player_motion loco

# 나비아 금빛 카드 효과(fx/nv/init 의 점수판 · 저장소; 카드 자체는 rlk_room 으로 위에서 지운다)
scoreboard objectives remove nvfx
scoreboard objectives remove nvfxT
scoreboard objectives remove nvfxD
scoreboard objectives remove nvfxK
data remove storage rlk:nvfx a

# 화면 미니맵
bossbar remove rlk:minimap
scoreboard objectives remove mm

# 리소스팩 보스바
scoreboard objectives remove bu
scoreboard objectives remove buTrail
scoreboard objectives remove buLast
scoreboard objectives remove buT
