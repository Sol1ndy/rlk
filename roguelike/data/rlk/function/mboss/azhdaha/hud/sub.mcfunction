# The sub-line (plan 4.11), first match: intro name, "마지막 일격!", the jump cue, B3 "꼬리만 공격할 수 있습니다",
# the transition message, a hint, the running pattern; then the brand part and any pattern-provided part
# (storage az.subx, e.g. 42's "안전 지대 N칸").
data modify storage rlk:mboss sub set value []
execute if score #mbSt mb matches 0 run return run data modify storage rlk:mboss sub set value [{text:"봉인된 바위 용의 왕",color:"#E8E2D0",bold:true}]
function rlk:mboss/azhdaha/hud/sub_main
function rlk:mboss/azhdaha/brand/hud
execute if data storage rlk:mboss az.hud.br run data modify storage rlk:mboss sub append from storage rlk:mboss az.hud.br[]
execute if data storage rlk:mboss az.subx run data modify storage rlk:mboss sub append from storage rlk:mboss az.subx[]
