# rootc 의 카드마다 함께 줄 아이템 → rlk:room rooti
data modify storage rlk:room rooti set value []
data modify storage rlk:room iq set from storage rlk:room rootc
function rlk:root/items_loop
