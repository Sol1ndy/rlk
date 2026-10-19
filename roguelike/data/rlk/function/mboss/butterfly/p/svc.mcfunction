# Core mechanics on the service patterns' clocks (their pattern files own only fx and hazards):
# transformation clock 5 = the light sphere (달빛 고치, 달빛 이슬); 달빛 해제 clock 0 = its caption,
# 74 = the wings go flat lime, 79 = she is human again (hitbox, heal orbs vanish).
execute if score #bfPat mb matches 20 if score #bfPT mb matches 5 run return run function rlk:mboss/butterfly/form/sphere
execute if score #bfPat mb matches 15 if score #bfPT mb matches 0 run return run function rlk:mboss/line/say {t:"달빛 해제",c:"#D9F5A8",gap:2,hold:30,snd:2}
execute if score #bfPat mb matches 15 if score #bfPT mb matches 74 run return run function rlk:mboss/butterfly/rig/look/flat
execute if score #bfPat mb matches 15 if score #bfPT mb matches 79 run return run function rlk:mboss/butterfly/form/revert
