# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** 01 **Thành viên:** 1. Phạm Quang Huy - 2A202602900, 2. Ngô Đức Chung - 2A202602985

Detector cố định: `yolo26n.pt`, ảnh 640 px, Re-ID `osnet_x0_25_msmt17`. Không đổi các mục này trong bài nộp chính.

File nộp: `runs/nop_bai/video_1.txt` … `video_5.txt`, chạy đủ frame (600 / 1050 / 837 / 900 / 750), kèm `video_N_preview.mp4` để xem ID.

## 1. Cấu hình đã chọn

Mỗi video: tracker bạn nộp, `conf`, `iou`, điều bạn **nhìn thấy** trên video, và một cấu hình đã thử rồi loại.

| Video | Tracker | conf | iou | Quan sát khi xem video | Đã thử nhưng loại |
|---|---|---|---|---|---|
| video_1 (quảng trường, tĩnh, ban ngày) | `botsort` | 0.3 | 0.7 | Hai người đứng gần camera (áo xanh nhạt, áo tím) giữ nguyên ID suốt f250–340; người đi ngang qua phải giữ một ID. Rất ít hộp giả (Precision 88%). Phần lớn người nhỏ ở hậu cảnh không có hộp: detector bỏ sót, Recall chỉ 22%. | `strongsort` c0.15 i0.4: IDF1 cao nhất (32.7) nhưng 174 ID cho 62 người, ID nhảy số liên tục ở hậu cảnh, HOTA 29.2. `bytetrack` c0.3: ít đổi ID (12) nhưng bỏ sót nhiều, HOTA 26.9. |
| video_2 (phố đêm, tĩnh, rất đông) | `botsort` | 0.15 | 0.7 | conf thấp bắt thêm người mờ dưới ánh đèn (ông vest xám, người cạnh bãi xe đạp) mà conf 0.3 bỏ sót. Người đội mũ giữ ID 19, áo hồng 26 suốt f300–420. Người áo trắng (13) và một người đi ngang (43) cắt nhau ở f340, hai hộp trùng nhau, rồi tách ra vẫn đúng ID. Đám đông nhỏ phía trên vẫn phần lớn không có hộp. Trong các đoạn đã xem không thấy hộp giả trên cột đèn hay cọc giao thông. | `botsort` c0.3 i0.5: mất hẳn hộp người đội mũ ở f340, bỏ sót ông vest xám. `bytetrack` c0.3: người đội mũ mất hộp ở f340 rồi quay lại với ID mới (13→30); cặp người bên phải bị gộp vào một hộp. `ocsort` c0.3: người áo trắng đổi ID 8→45 ở f380. |
| video_3 (camera di động, ảnh nhỏ) | `ocsort` | 0.5 | 0.5 | Người đi ngay trước camera chiếm nửa khung, che người phía sau liên tục. Người quần trắng băng ngang phía sau giữ ID 72 (f512–524). Người bên phải giữ ID 8 sau khi bị xe hơi chạy ngang che (f100–132). Vẫn nhiều mảnh track (114 ID, track trung vị 16 frame). | `botsort` c0.3: đổi ID 181→184 đúng lúc người quần trắng băng ngang, 169 ID; thử thêm c0.15 và c0.5 vẫn 146–161 ID. `ocsort` c0.15: 223 ID, mỗi hộp yếu mở một track rác. |
| video_4 (trong nhà, camera di chuyển) | `botsort` | 0.15 | 0.5 | Người áo đỏ đi trước camera giữ ID 2 suốt f100–500; người áo trắng giữ ID 46 (f400–500). Bóng chân phản chiếu trên kính lan can không bị gán hộp. Hộp nằm trong vùng kính (f94) là người thật đi thang cuốn ở tầng dưới. | `bytetrack` c0.15: ít ID nhất (56) nhưng thiếu 7.6% số hộp so với BoT-SORT; đã xem từng hộp thiếu, đều là người bị che một phần hoặc ở xa. `bytetrack` c0.3: người khuất sau người áo đỏ đổi ID 16→23 (f100→130); ở c0.15 người này giữ nguyên ID. |
| video_5 (trên xe bus, giao lộ đông) | `botsort` | 0.15 | 0.5 | Xe bus đi qua giao lộ, cảnh rung và trôi. Người quần đỏ giữ ID 90, người áo khoác trắng giữ ID 97 suốt f300–340. Đám đông băng qua đường phần lớn không có hộp vì người quá nhỏ ở 640 px. | `ocsort` c0.3: người quần đỏ đổi 66→74, sau đó ID 66 nhảy sang người áo trắng (gán nhầm). `bytetrack` c0.3: người đàn ông to, rõ ở f280 không có ID; chỉ 2.7 hộp/frame, hạ c0.15 vẫn 2.9. `botsort` c0.3: bỏ sót người áo trắng ở f320. |

## 2. Số liệu video_1

Dán bảng HOTA / MOTA / IDF1 do `scripts/evaluate_practice.py` in ra.

```
python scripts/evaluate_practice.py --trackeval-root TrackEval --lab-data-root lab_data \
    --submission runs/nop_bai/video_1.txt --run-name nhom01_video1

HOTA: nhom01_video1-pedestrian     HOTA      DetA      AssA      DetRe     DetPr     AssRe     AssPr     LocA      OWTA      HOTA(0)   LocA(0)   HOTALocA(0)
video_1                            30        18.425    49.112    19.152    75.045    52.434    80.969    83.065    30.622    37.162    76.935    28.591
COMBINED                           30        18.425    49.112    19.152    75.045    52.434    80.969    83.065    30.622    37.162    76.935    28.591

CLEAR: nhom01_video1-pedestrian    MOTA      MOTP      MODA      CLR_Re    CLR_Pr    MTR       PTR       MLR       sMOTA     CLR_TP    CLR_FN    CLR_FP    IDSW      MT        PT        ML        Frag
video_1                            19.283    80.808    19.461    22.491    88.127    14.516    17.742    67.742    14.967    4179      14402     563       33        9         11        42        105
COMBINED                           19.283    80.808    19.461    22.491    88.127    14.516    17.742    67.742    14.967    4179      14402     563       33        9         11        42        105

Identity: nhom01_video1-pedestrian IDF1      IDR       IDP       IDTP      IDFN      IDFP
video_1                            29.747    18.67     73.155    3469      15112     1273
COMBINED                           29.747    18.67     73.155    3469      15112     1273

Count: nhom01_video1-pedestrian    Dets      GT_Dets   IDs       GT_IDs
video_1                            4742      18581     54        62
COMBINED                           4742      18581     54        62
```

Tóm tắt: **HOTA 30.00, MOTA 19.28, IDF1 29.75**. AssA (49.1) cao gấp gần ba lần DetA (18.4): phần giữ danh tính đã ổn, phần kéo điểm xuống là phát hiện. 42/62 người bị bỏ sót gần hết (ML), 14 402 hộp nhãn không được phát hiện, trong khi chỉ có 563 hộp giả và 33 lần đổi ID.

So sánh các cấu hình đã chạy đủ frame trên video_1, sắp theo HOTA (23 lượt, trích các dòng chính):

| Tracker | conf | iou | HOTA | DetA | AssA | MOTA | IDF1 | IDSW | Số ID |
|---|---|---|---|---|---|---|---|---|---|
| **botsort** | **0.3** | **0.7** | **30.00** | 18.43 | 49.11 | 19.28 | 29.75 | 33 | 54 |
| botsort | 0.15 | 0.7 | 29.67 | 19.43 | 45.67 | 20.31 | 29.87 | 37 | 58 |
| botsort | 0.1 | 0.5 | 29.52 | 19.55 | 44.97 | 21.00 | 30.28 | 23 | 56 |
| botsort | 0.3 | 0.5 | 29.46 | 18.09 | 48.24 | 19.81 | 29.34 | 25 | 52 |
| botsort | 0.3 | 0.4 | 29.32 | 17.36 | 49.64 | 19.47 | 29.80 | 19 | 50 |
| strongsort | 0.15 | 0.4 | 29.21 | 21.54 | 40.18 | 20.24 | 32.68 | 92 | 174 |
| strongsort | 0.3 | 0.5 | 28.67 | 17.71 | 46.62 | 19.72 | 29.88 | 40 | 79 |
| strongsort | 0.15 | 0.7 | 28.42 | 22.00 | 37.49 | 17.75 | 32.42 | 214 | 269 |
| ocsort | 0.3 | 0.5 | 27.47 | 17.89 | 42.37 | 19.79 | 28.73 | 44 | 68 |
| deepocsort | 0.3 | 0.5 | 27.37 | 17.84 | 42.17 | 19.74 | 27.77 | 52 | 73 |
| bytetrack | 0.15 | 0.5 | 27.31 | 15.86 | 47.14 | 18.31 | 26.99 | 13 | 35 |
| botsort | 0.5 | 0.5 | 27.16 | 14.30 | 51.67 | 15.24 | 24.54 | 10 | 35 |
| bytetrack | 0.3 | 0.5 | 26.91 | 15.07 | 48.12 | 17.30 | 25.71 | 12 | 34 |
| ocsort | 0.15 | 0.5 | 25.62 | 21.59 | 30.94 | 19.43 | 28.64 | 169 | 150 |

`video_2` đến `video_5` không có nhãn trong gói lab. Không điền số cho các video đó.

## 3. Phân tích

**video_1: BoT-SORT, camera tĩnh, ban ngày.** Ba metric không chọn cùng một cấu hình: MOTA cao nhất là BoT-SORT c0.1 (21.0), IDF1 cao nhất là StrongSORT c0.15 (32.7), HOTA cao nhất là BoT-SORT c0.3 i0.7 (30.0). StrongSORT c0.15 có IDF1 cao vì bắt nhiều hộp hơn (DetA 21.5), nhưng tách 62 người thành 174 ID. Trên video thấy rõ: người ở hậu cảnh đổi số liên tục, nên AssA chỉ 40. BoT-SORT ghép hai vòng theo điểm hộp, có Re-ID và giữ track mất dấu tới 60 frame, nên người đứng gần camera giữ ID suốt đoạn bị che (AssA 49). `iou` 0.7 cho NMS giữ lại hộp của những người đứng sát nhau. So với i0.5, DetRe tăng từ 18.6 lên 19.2 và AssA từ 48.2 lên 49.1, đổi lại hộp giả tăng từ 337 lên 563 và IDSW từ 25 lên 33. HOTA vẫn nhỉnh hơn (29.46 → 30.00), nên nhóm chọn i0.7. Đây là chênh lệch nhỏ, không phải khác biệt lớn. Trần của bài này là detector: đổi tracker chỉ dịch HOTA trong khoảng 25–30, vì 2/3 số người gần như không bao giờ có hộp.

**video_3: OC-SORT, camera di động, ảnh nhỏ, FPS thấp (chỉ đánh giá bằng mắt).** Ngược với dự đoán ban đầu, các tracker có Re-ID (BoT-SORT, StrongSORT, DeepOCSORT) tạo nhiều ID hơn (146–169) so với OC-SORT c0.5 (114) và ByteTrack c0.3 (127). Ở f512→518, BoT-SORT đổi ID người quần trắng băng ngang phía sau, trong khi OC-SORT và ByteTrack giữ nguyên. Hai lý do khả dĩ. Thứ nhất, ở 640×480 vùng cắt mỗi người rất ít chi tiết nên đặc trưng Re-ID yếu. Thứ hai, người đi ngay trước camera chiếm nửa khung hình, nên phần bù chuyển động camera (optical flow) của BoT-SORT bám vào người đó thay vì nền. OC-SORT dùng hướng chuyển động thực sự quan sát được và cập nhật lại Kalman khi track tái xuất hiện, nên nối lại được người sau khi bị xe hơi che (ID 8 ở f100–132). `conf` 0.5 là bắt buộc với OC-SORT ở đây: cấu hình mặc định mở track cho mọi hộp, nên c0.15 sinh tới 223 ID.

**video_5: BoT-SORT, trên xe bus, rung lắc (chỉ đánh giá bằng mắt).** Khi xe bus rẽ, mọi người trong ảnh trôi theo camera. Bộ dự đoán Kalman thuần chuyển động đoán sai vị trí, nên OC-SORT để ID 66 nhảy từ người quần đỏ sang người áo trắng bên cạnh. BoT-SORT bù chuyển động camera trước khi ghép, rồi dùng Re-ID để xác nhận. Nhờ vậy người quần đỏ giữ ID 90 suốt đoạn xe qua giao lộ. ByteTrack gần như không dùng được ở cảnh này: nó chỉ mở track mới từ hộp có điểm ≥ 0.5, mà người đi bộ nhìn từ tầng trên xe bus nhỏ và hiếm khi đạt ngưỡng đó. Vì vậy hạ `--conf` từ 0.3 xuống 0.15 chỉ tăng từ 2.7 lên 2.9 hộp/frame, còn BoT-SORT c0.15 được 4.4.

**video_2: BoT-SORT, phố đêm, rất đông (chỉ đánh giá bằng mắt).** Ban đêm điểm tin cậy của người ở vùng tối thấp hơn, nên `conf` 0.15 cứu thêm vài người mà conf 0.3 bỏ sót. Hạ conf ở BoT-SORT an toàn vì nó chỉ mở track mới từ hộp > 0.34. Hộp 0.15–0.34 chỉ dùng để nối track sẵn có, nên số ID gần như không đổi (62–63, so với 125 của OC-SORT c0.15). Camera tĩnh nên phần bù chuyển động không giúp gì nhiều. Lợi thế đến từ Re-ID và ghép hai vòng. Ở f340, người đội mũ có điểm hộp tụt xuống. BoT-SORT c0.3 mất hẳn người này, ByteTrack mất rồi cấp ID mới, còn BoT-SORT c0.15 vẫn nối được bằng hộp điểm thấp và giữ ID 19. Cũng ở f340, hai người cắt nhau (ID 13 và 43) tới mức hai hộp trùng nhau, rồi tách ra vẫn đúng ID. Đây là chỗ đặc trưng ngoại hình giúp phân biệt hai người.

**Ghi chú phương pháp cho video không nhãn.** Ngoài xem video, nhóm đếm thêm "track sinh giữa ảnh": track mới mà hộp đầu tiên cao hơn 20% khung hình và không chạm mép trái/phải. Một người to đứng giữa ảnh không thể tự dưng xuất hiện, nên phần lớn các track này là đổi ID. Trên video_1, chỉ số này xếp hạng gần giống IDSW thật (StrongSORT tệ nhất, BoT-SORT c0.3 i0.4 tốt nhất). Vì vậy nhóm dùng nó làm bằng chứng phụ, không thay cho việc xem video.

## 4. Nếu có thêm thời gian (Thực nghiệm mở rộng / Bonus)

Nhóm đã tiến hành thực nghiệm mở rộng ngoài bài nộp chính: **tăng kích thước ảnh đầu vào của detector lên 1280 px** (thay vì 640 px cố định) với cấu hình đã chọn `botsort` (conf 0.3, iou 0.7) trên `video_1`:

| Kích thước ảnh | HOTA | DetA | AssA | MOTA | IDF1 | CLR_TP | CLR_FN | IDSW | ML |
|---|---|---|---|---|---|---|---|---|---|
| **640 px (bài nộp chính)** | 30.00 | 18.43 | 49.11 | 19.28 | 29.75 | 4,179 | 14,402 | 33 | 42/62 |
| **1280 px (Bonus mở rộng)** | **32.37** | **27.61** | 38.53 | **28.10** | **39.43** | **6,445** | **12,136** | 95 | **32/62** |

**Kết luận thực nghiệm:**
- Đúng như chẩn đoán, **detector chính là nút thắt cổ chai lớn nhất**. Khi tăng lên 1280 px, số hộp phát hiện đúng (TP) tăng vọt thêm **+2,266 hộp**, DetA tăng từ 18.43% lên 27.61% (+9.18%), kéo theo **MOTA tăng mạnh từ 19.28 lên 28.10** (+8.82 điểm) và **IDF1 tăng từ 29.75 lên 39.43** (+9.68 điểm). Số người bị mất dấu hoàn toàn (ML) giảm từ 42 xuống 32 người.
- Nếu có thêm thời gian, nhóm sẽ kết hợp chỉnh thêm tham số nội bộ tracker (`track_high_thresh` của BoT-SORT cho cảnh đêm và `max_age` của OC-SORT cho cảnh di động FPS thấp) để giảm bớt số lần IDSW phát sinh từ các track nhỏ ở xa.
