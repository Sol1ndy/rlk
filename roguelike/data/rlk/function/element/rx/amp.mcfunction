# 증폭 반응 (증발/융해). macro: e(소모할 부착 원소), use(소모량 %: 강한 쪽이 때리면 200, 약한 쪽이 때리면 50), mul(피해 배율 %), rx
$function rlk:element/use {e:"$(e)",m:$(use)}
$scoreboard players set #mulPct tmp $(mul)
$scoreboard players set #rx tmp $(rx)
