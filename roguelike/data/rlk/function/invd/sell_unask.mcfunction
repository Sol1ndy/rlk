# 판매 버튼에서 조준을 떼면 되묻기 취소
scoreboard players set @s pkConf 0
data modify entity @e[tag=rlk_invd_sell,limit=1] text set value [{text:" 판매 ",color:"#FFE08A"},{text:"◆ ",color:"#E0B255"},{score:{name:"#invdPrice",objective:"tmp"},color:"#E0B255"},{text:" "}]
