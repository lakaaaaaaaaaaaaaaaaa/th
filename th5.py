def tinh_giai_thua(n):
    if n < 0:
        return "Lỗi: Không tính giai thừa cho số âm."
    if n == 0 or n == 1:
        return 1
    
    ket_qua = 1
    for i in range(2, n + 1):
        ket_qua *= i
    return ket_qua

# Thử nghiệm với n = 5
print(f"Giai thừa của 5 là: {tinh_giai_thua(5)}") # Kết quả: 120
def tinh_trung_binh(danh_sach):
    if not danh_sach:
        return 0
    return sum(danh_sach) / len(danh_sach)

# Thử nghiệm với một dãy số giao dịch
giao_dich = [150.0, 200.5, 300.0, 50.25]
print(f"Giá trị trung bình: {tinh_trung_binh(giao_dich):.2f}")
def tinh_loi_nhuan_12_thang(von_ban_dau, lai_suat_thang):
    # lai_suat_thang nên ở dạng thập phân (ví dụ: 0.5% = 0.005)
    tong_tien = von_ban_dau * (1 + lai_suat_thang)**12
    loi_nhuan = tong_tien - von_ban_dau
    
    return tong_tien, loi_nhuan

# Giả sử gửi 100 triệu với lãi suất 0.6%/tháng
von = 100000000
lai = 0.006

tong, loi = tinh_loi_nhuan_12_thang(von, lai)

print(f"--- Báo cáo tài chính sau 1 năm ---")
print(f"Vốn ban đầu: {von:,.0f} VND")
print(f"Lợi nhuận ròng: {loi:,.0f} VND")
print(f"Tổng số dư: {tong:,.0f} VND")