# The break meter line: [badge] 역장  [20 pips in groups of five]  n/20 (font rlk:mboss_fg of the fx kit),
# the running field pattern, the first field's hint. Rebuilt only on a change (count, pip flash end, state).
data modify storage rlk:mboss sub set value [{text:"",font:"rlk:mboss_fg",color:"white"},{text:" 역장  ",color:"#C58BFF",bold:true}]
execute if score #fgPipT mb matches 1.. run function rlk:mboss/fieldgen/hud/pipsf_d
execute unless score #fgPipT mb matches 1.. run function rlk:mboss/fieldgen/hud/pips_d
execute if score #fgSt mb matches 1 if score #fgPat mb matches 11 run data modify storage rlk:mboss sub append value {text:"   · 중력 시스템·감소 영역",color:"#BFAEE8",bold:false}
execute if score #fgSt mb matches 1 if score #fgPat mb matches 12 run data modify storage rlk:mboss sub append value {text:"   · 중력 시스템·파쇄",color:"#BFAEE8",bold:false}
execute if score #fgSt mb matches 1 if score #fgPat mb matches 21 run data modify storage rlk:mboss sub append value {text:"   · 「인력 충격파」",color:"#BFAEE8",bold:false}
execute if score #fgSt mb matches 1 if score #fgPat mb matches 22 run data modify storage rlk:mboss sub append value {text:"   · 역장 해제",color:"#BFAEE8",bold:false}
execute if score #fgFN mb matches 1 if score #fgHintT mb matches ..119 run data modify storage rlk:mboss sub append value {text:"   코어를 공격해 역장을 깨뜨리세요",color:"#E8D8FF",bold:false}
