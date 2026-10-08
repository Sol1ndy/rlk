# macro: key. 슬롯 표시 기록(접힘=이름, 펼침=이름+설명)
$data modify storage rlk:shop records.k$(key) set value {}
$data modify storage rlk:shop records.k$(key).col set from storage rlk:io name
$data modify storage rlk:shop records.k$(key).full set from storage rlk:io dfull
