from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime
from django.db.models import Sum

class KhuVuc(models.Model):
    id_khu_vuc = models.AutoField(primary_key=True)
    ten_khu_vuc = models.CharField(max_length=25)
    
    class Meta:
        db_table = 'khu_vuc'
        verbose_name = 'Khu vực'
        verbose_name_plural = 'Khu vực'

class QuocGia(models.Model):
    id_quoc_gia = models.CharField(max_length=2, primary_key=True)
    ten_quoc_gia = models.CharField(max_length=40, null=True)
    id_khu_vuc = models.ForeignKey(KhuVuc, on_delete=models.CASCADE, db_column='id_khu_vuc')
    
    class Meta:
        db_table = 'quoc_gia'
        verbose_name = 'Quốc gia'
        verbose_name_plural = 'Quốc gia'

class DiaDiem(models.Model):
    id_dia_diem = models.AutoField(primary_key=True)
    dia_chi_duong = models.CharField(max_length=40, null=True)
    ma_buu_dien = models.CharField(max_length=12, null=True)
    thanh_pho = models.CharField(max_length=30)
    tinh_thanh = models.CharField(max_length=25, null=True)
    id_quoc_gia = models.ForeignKey(QuocGia, on_delete=models.CASCADE, db_column='id_quoc_gia')
    
    class Meta:
        db_table = 'dia_diem'
        verbose_name = 'Địa điểm'
        verbose_name_plural = 'Địa điểm'

class CongViec(models.Model):
    id_cong_viec = models.AutoField(primary_key=True)
    ten_cong_viec = models.CharField(max_length=35)
    luong_toi_thieu = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    luong_toi_da = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    
    class Meta:
        db_table = 'cong_viec'
        verbose_name = 'Công việc'
        verbose_name_plural = 'Công việc'

class PhongBan(models.Model):
    id_phong_ban = models.AutoField(primary_key=True)
    ten_phong_ban = models.CharField(max_length=30)
    id_dia_diem = models.ForeignKey(DiaDiem, on_delete=models.CASCADE, null=True, db_column='id_dia_diem')
    
    class Meta:
        db_table = 'phong_ban'
        verbose_name = 'Phòng ban'
        verbose_name_plural = 'Phòng ban'

class NhanVien(models.Model):
    id_nhan_vien = models.AutoField(primary_key=True)
    ho = models.CharField(max_length=30)
    ten = models.CharField(max_length=20)
    email = models.CharField(max_length=100, null=True, blank=True)
    so_dien_thoai = models.CharField(max_length=20, null=True)
    ngay_thue = models.DateField()
    id_cong_viec = models.ForeignKey(CongViec, on_delete=models.CASCADE, db_column='id_cong_viec')
    luong = models.DecimalField(max_digits=12, decimal_places=2)
    id_quan_ly = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='id_quan_ly')
    id_phong_ban = models.ForeignKey(PhongBan, on_delete=models.CASCADE, null=True, db_column='id_phong_ban')
    
    class Meta:
        db_table = 'nhan_vien'
        verbose_name = 'Nhân viên'
        verbose_name_plural = 'Nhân viên'

class NguoiPhuThuoc(models.Model):
    id_nguoi_phu_thuoc = models.AutoField(primary_key=True)
    ho = models.CharField(max_length=30)
    ten = models.CharField(max_length=20)
    quan_he = models.CharField(max_length=25)
    id_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column='id_nhan_vien')
    
    class Meta:
        db_table = 'nguoi_phu_thuoc'
        verbose_name = 'Người phụ thuộc'
        verbose_name_plural = 'Người phụ thuộc'

class Attendance(models.Model):
    id_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column='id_nhan_vien')
    ngay_lam = models.DateField(auto_now_add=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    gio_lam = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    ngay_cong = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'attendance'
        unique_together = ('id_nhan_vien', 'ngay_lam')
        ordering = ['-ngay_lam']
        verbose_name = 'Chấm công'
        verbose_name_plural = 'Chấm công'
    
    def save(self, *args, **kwargs):
        # Tự động tính gio_lam và ngay_cong khi có check_out
        if self.check_in and self.check_out:
            time_diff = self.check_out - self.check_in
            self.gio_lam = Decimal(str(time_diff.total_seconds() / 3600))
            self.ngay_cong = round(self.gio_lam / 8, 2)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id_nhan_vien.ho} {self.id_nhan_vien.ten} - {self.ngay_lam}"

class PayrollRecord(models.Model):
    id_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column='id_nhan_vien')
    thang = models.DateField()  # Lưu ngày đầu tháng
    tong_ngay_lam = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    luong_thuc_nhan = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ngay_tinh = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payrollrecord'
        unique_together = ('id_nhan_vien', 'thang')
        ordering = ['-thang']
        verbose_name = 'Bảng lương'
        verbose_name_plural = 'Bảng lương'
    
    def calculate_total_days(self):
        # Lấy tháng và năm từ trường thang
        month = self.thang.month
        year = self.thang.year
        
        # Tính tổng số ngày công từ bảng Attendance
        total_days = Attendance.objects.filter(
            id_nhan_vien=self.id_nhan_vien,
            ngay_lam__year=year,
            ngay_lam__month=month
        ).aggregate(total=Sum('ngay_cong'))['total'] or 0
        
        return total_days
    
    def save(self, *args, **kwargs):
        # Tính tổng số ngày làm từ bảng chấm công
        self.tong_ngay_lam = self.calculate_total_days()
        
        # Tính lương thực nhận dựa trên số ngày làm
        if self.tong_ngay_lam > 0:
            self.luong_thuc_nhan = round(self.tong_ngay_lam * (self.id_nhan_vien.luong / 22), 2)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id_nhan_vien.ho} {self.id_nhan_vien.ten} - {self.thang.strftime('%m/%Y')}"