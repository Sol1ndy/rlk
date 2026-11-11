# Resource pack snapshots (outside the main tree)

The resource pack is not in git (README 0-4). This orphan branch keeps release zips so a new container can restore them.

| file | release | sha1 of the unpacked tree |
|---|---|---|
| rlk_hud_resourcepack_1106.zip | 11-06 홍련 · 특수 보스 (stamp c77e5d1) | b3df6a5f0476cb71426fad61e8c5d3878aac4878 (4 769 files) |
| rlk_hud_resourcepack_1111.zip | 11-11 전투 개편 (stamp c9eed47) | 91d7a9fdc2167f89fd6bdb685f11cb8c5d507cbc (4 776 files) |
| rlk_hud_resourcepack_1111b.zip | 11-11b 홍련 재완성 (stamp 74f89e3) | a342db3b052ad9d445c3ae0e5975429ebb82a7b0 (4 871 files) |

Restore the newest: `unzip rlk_hud_resourcepack_1111b.zip -d <rp folder>`.
