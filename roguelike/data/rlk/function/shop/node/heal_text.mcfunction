# macro: name, pct, color → io.name / io.dfull (이름 + 설명)
$data modify storage rlk:io name set value {text:"$(name)",color:"$(color)",italic:false}
data modify storage rlk:io dfull set value []
data modify storage rlk:io dfull append from storage rlk:io name
$data modify storage rlk:io dfull append value {text:"\n최대 체력의 $(pct)%를 회복한다",color:"#D0D0D0",italic:false}
data modify storage rlk:io dfull append value {text:"\n(체력이 가득하면 살 수 없음)",color:"dark_gray",italic:false}
