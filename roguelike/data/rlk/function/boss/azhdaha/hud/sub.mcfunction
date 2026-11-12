# The sub-line (plan 4.11), first match: intro name, "마지막 일격!", the transition message, the running
# pattern; then the brand part and any pattern-provided part (storage az.subx). No advice lines (user rule
# 10-21: no in-game tips; the transition message is Genshin's own prompt).
data modify storage rlk:mboss sub set value []
execute if score #mbSt mb matches 0 run return run data modify storage rlk:mboss sub set value [{text:"봉인된 바위 용의 왕",color:"#E8E2D0",bold:true}]
function rlk:boss/azhdaha/hud/sub_main
function rlk:boss/azhdaha/brand/hud
execute if data storage rlk:mboss az.hud.br run data modify storage rlk:mboss sub append from storage rlk:mboss az.hud.br[]
execute if data storage rlk:mboss az.subx run data modify storage rlk:mboss sub append from storage rlk:mboss az.subx[]
