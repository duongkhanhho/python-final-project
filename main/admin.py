from django.contrib import admin
from .models import (
    KhuVuc, QuocGia, DiaDiem, CongViec, PhongBan, 
    NhanVien, NguoiPhuThuoc, Attendance, PayrollRecord
)


@admin.register(KhuVuc)
class KhuVucAdmin(admin.ModelAdmin):
    list_display = ('id_khu_vuc', 'ten_khu_vuc')
    search_fields = ('ten_khu_vuc',)


@admin.register(QuocGia)
class QuocGiaAdmin(admin.ModelAdmin):
    list_display = ('id_quoc_gia', 'ten_quoc_gia', 'ten_khu_vuc')
    list_filter = ('id_khu_vuc',)
    search_fields = ('ten_quoc_gia', 'id_quoc_gia')
    
    def ten_khu_vuc(self, obj):
        return obj.id_khu_vuc.ten_khu_vuc if obj.id_khu_vuc else '-'
    ten_khu_vuc.short_description = 'Khu vực'


@admin.register(DiaDiem)
class DiaDiemAdmin(admin.ModelAdmin):
    list_display = ('id_dia_diem', 'dia_chi_duong', 'thanh_pho', 'tinh_thanh', 'ten_quoc_gia')
    list_filter = ('id_quoc_gia', 'tinh_thanh')
    search_fields = ('thanh_pho', 'tinh_thanh', 'dia_chi_duong')
    
    def ten_quoc_gia(self, obj):
        return obj.id_quoc_gia.ten_quoc_gia if obj.id_quoc_gia else '-'
    ten_quoc_gia.short_description = 'Quốc gia'


@admin.register(CongViec)
class CongViecAdmin(admin.ModelAdmin):
    list_display = ('id_cong_viec', 'ten_cong_viec', 'luong_toi_thieu_vnd', 'luong_toi_da_vnd')
    search_fields = ('ten_cong_viec',)
    
    def luong_toi_thieu_vnd(self, obj):
        if obj.luong_toi_thieu:
            return f"{obj.luong_toi_thieu:,.0f} VND"
        return '-'
    luong_toi_thieu_vnd.short_description = 'Lương tối thiểu'
    
    def luong_toi_da_vnd(self, obj):
        if obj.luong_toi_da:
            return f"{obj.luong_toi_da:,.0f} VND"
        return '-'
    luong_toi_da_vnd.short_description = 'Lương tối đa'


@admin.register(PhongBan)
class PhongBanAdmin(admin.ModelAdmin):
    list_display = ('id_phong_ban', 'ten_phong_ban', 'ten_dia_diem')
    list_filter = ('id_dia_diem',)
    search_fields = ('ten_phong_ban',)
    
    def ten_dia_diem(self, obj):
        return obj.id_dia_diem.thanh_pho if obj.id_dia_diem else '-'
    ten_dia_diem.short_description = 'Địa điểm'


@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ('id_nhan_vien', 'ho', 'ten', 'email', 'ten_cong_viec', 'ten_phong_ban', 'luong_vnd')
    list_filter = ('id_cong_viec', 'id_phong_ban', 'ngay_thue')
    search_fields = ('ho', 'ten', 'email')
    date_hierarchy = 'ngay_thue'
    
    def ten_cong_viec(self, obj):
        return obj.id_cong_viec.ten_cong_viec if obj.id_cong_viec else '-'
    ten_cong_viec.short_description = 'Công việc'
    
    def ten_phong_ban(self, obj):
        return obj.id_phong_ban.ten_phong_ban if obj.id_phong_ban else '-'
    ten_phong_ban.short_description = 'Phòng ban'
    
    def luong_vnd(self, obj):
        if obj.luong:
            return f"{obj.luong:,.0f} VND"
        return '-'
    luong_vnd.short_description = 'Lương'


@admin.register(NguoiPhuThuoc)
class NguoiPhuThuocAdmin(admin.ModelAdmin):
    list_display = ('id_nguoi_phu_thuoc', 'ho', 'ten', 'quan_he', 'ten_nhan_vien')
    list_filter = ('quan_he',)
    search_fields = ('ho', 'ten', 'quan_he')
    
    def ten_nhan_vien(self, obj):
        return f"{obj.id_nhan_vien.ho} {obj.id_nhan_vien.ten}" if obj.id_nhan_vien else '-'
    ten_nhan_vien.short_description = 'Nhân viên'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('ten_nhan_vien', 'ngay_lam_formatted', 'check_in_formatted', 'check_out_formatted', 'gio_lam_formatted', 'ngay_cong_formatted')
    list_filter = ('ngay_lam', 'id_nhan_vien__id_phong_ban')
    search_fields = ('id_nhan_vien__ho', 'id_nhan_vien__ten')
    date_hierarchy = 'ngay_lam'
    readonly_fields = ('gio_lam', 'ngay_cong')
    
    def ten_nhan_vien(self, obj):
        return f"{obj.id_nhan_vien.ho} {obj.id_nhan_vien.ten}" if obj.id_nhan_vien else '-'
    ten_nhan_vien.short_description = 'Tên nhân viên'
    
    def ngay_lam_formatted(self, obj):
        return obj.ngay_lam.strftime('%d/%m/%Y') if obj.ngay_lam else '-'
    ngay_lam_formatted.short_description = 'Ngày làm'
    
    def check_in_formatted(self, obj):
        return obj.check_in.strftime('%d/%m/%Y %H:%M') if obj.check_in else '-'
    check_in_formatted.short_description = 'Giờ vào'
    
    def check_out_formatted(self, obj):
        return obj.check_out.strftime('%d/%m/%Y %H:%M') if obj.check_out else '-'
    check_out_formatted.short_description = 'Giờ ra'
    
    def gio_lam_formatted(self, obj):
        return f"{obj.gio_lam:.1f}h" if obj.gio_lam else '-'
    gio_lam_formatted.short_description = 'Số giờ làm'
    
    def ngay_cong_formatted(self, obj):
        return f"{obj.ngay_cong:.2f}" if obj.ngay_cong else '-'
    ngay_cong_formatted.short_description = 'Số công'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('id_nhan_vien')


@admin.register(PayrollRecord)
class PayrollRecordAdmin(admin.ModelAdmin):
    list_display = ('ten_nhan_vien', 'thang_formatted', 'tong_ngay_lam_formatted', 'luong_thuc_nhan_vnd', 'ngay_tinh_formatted')
    list_filter = ('thang', 'id_nhan_vien__id_phong_ban')
    search_fields = ('id_nhan_vien__ho', 'id_nhan_vien__ten')
    date_hierarchy = 'thang'
    readonly_fields = ('luong_thuc_nhan', 'ngay_tinh')
    
    def ten_nhan_vien(self, obj):
        return f"{obj.id_nhan_vien.ho} {obj.id_nhan_vien.ten}" if obj.id_nhan_vien else '-'
    ten_nhan_vien.short_description = 'Tên nhân viên'
    
    def thang_formatted(self, obj):
        return obj.thang.strftime('%d/%m/%Y') if obj.thang else '-'
    thang_formatted.short_description = 'Tháng'
    
    def tong_ngay_lam_formatted(self, obj):
        return f"{obj.tong_ngay_lam:.2f}" if obj.tong_ngay_lam else '-'
    tong_ngay_lam_formatted.short_description = 'Số ngày làm'
    
    def luong_thuc_nhan_vnd(self, obj):
        if obj.luong_thuc_nhan:
            return f"{obj.luong_thuc_nhan:,.0f} VND"
        return '-'
    luong_thuc_nhan_vnd.short_description = 'Lương thực nhận'
    
    def ngay_tinh_formatted(self, obj):
        return obj.ngay_tinh.strftime('%d/%m/%Y %H:%M') if obj.ngay_tinh else '-'
    ngay_tinh_formatted.short_description = 'Ngày tính'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('id_nhan_vien')
