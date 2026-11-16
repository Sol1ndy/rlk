# The event title at E56 (seq/event; @s any): the item's name + its own stars (dark_red, a light shadow; <= 106 font px
# at 4x) / 「[ MYTHIC ]」 + its notice, or the buff's name / the first two numbers (subtitle <= 192 font px) + the third on
# the actionbar (hudHold); held 54 t (vBig / ttlT pause the F5 crosshair title). F3: HR-33, HR-35.
title @a[tag=player] times 6 44 4
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/ev/stars
execute if score #hrEv hr matches 1 run title @a[tag=player] subtitle {text:"",extra:[{text:"[ MYTHIC ]",color:"dark_red",shadow_color:-8730},{text:" 신화 아이템을 얻었습니다",color:"#E8E2D0"}]}
execute if score #hrEv hr matches 1 run title @a[tag=player] title {text:"화무십일홍",color:"dark_red",shadow_color:-8730,extra:[{nbt:"ev.sx",storage:"rlk:hr",interpret:true}]}
execute if score #hrEv hr matches 2 run title @a[tag=player] subtitle {text:"",color:"#FFE08A",extra:[{text:"최종 공격력 +"},{score:{name:"#hrMoonAtk",objective:"tmp"}},{text:"% · 치명타 확률 +"},{score:{name:"#hrMoonCrit",objective:"tmp"}},{text:"%"}]}
execute if score #hrEv hr matches 2 run title @a[tag=player] title {text:"월하대작",color:"#DDE6FF",bold:true}
execute if score #hrEv hr matches 2 run title @a[tag=player] actionbar {text:"",color:"#FFE08A",extra:[{text:"이동 속도 +"},{score:{name:"#hrMoonSpd",objective:"tmp"}},{text:"%"}]}
execute if score #hrEv hr matches 2 run scoreboard players set @a[tag=player] hudHold 54
scoreboard players set @a[tag=player] vBig 54
scoreboard players set @a[tag=player] ttlT 54
