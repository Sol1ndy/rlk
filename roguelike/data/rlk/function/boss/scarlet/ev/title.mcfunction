# The event title at E56 (seq/event; @s any): the item's display name (dark_red, a light shadow) / its notice, or the
# buff's name / numbers; held 54 t (vBig / ttlT pause the F5 crosshair title).
title @a[tag=player] times 6 44 4
execute if score #hrEv hr matches 1 run title @a[tag=player] subtitle {text:"신화 아이템을 얻었습니다",color:"#E8E2D0"}
execute if score #hrEv hr matches 1 run title @a[tag=player] title {text:"[ MYTHIC ] 화무십일홍 ★☆☆",color:"dark_red",shadow_color:-8730}
execute if score #hrEv hr matches 2 run title @a[tag=player] subtitle ["",{text:"최종 공격력 +",color:"#FFE08A"},{score:{name:"#hrMoonAtk",objective:"tmp"},color:"#FFE08A"},{text:"% · 치명타 확률 +",color:"#FFE08A"},{score:{name:"#hrMoonCrit",objective:"tmp"},color:"#FFE08A"},{text:"% · 이동 속도 +",color:"#FFE08A"},{score:{name:"#hrMoonSpd",objective:"tmp"},color:"#FFE08A"},{text:"%",color:"#FFE08A"}]
execute if score #hrEv hr matches 2 run title @a[tag=player] title {text:"월하대작",color:"#DDE6FF",bold:true}
scoreboard players set @a[tag=player] vBig 54
scoreboard players set @a[tag=player] ttlT 54
