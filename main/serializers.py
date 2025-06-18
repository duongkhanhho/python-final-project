from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import (
    KhuVuc, QuocGia, DiaDiem, CongViec, PhongBan, 
    NhanVien, NguoiPhuThuoc, Attendance, PayrollRecord
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class KhuVucSerializer(serializers.ModelSerializer):
    class Meta:
        model = KhuVuc
        fields = '__all__'


class QuocGiaSerializer(serializers.ModelSerializer):
    ten_khu_vuc = serializers.CharField(source='id_khu_vuc.ten_khu_vuc', read_only=True)
    
    class Meta:
        model = QuocGia
        fields = '__all__'


class DiaDiemSerializer(serializers.ModelSerializer):
    ten_quoc_gia = serializers.CharField(source='id_quoc_gia.ten_quoc_gia', read_only=True)
    
    class Meta:
        model = DiaDiem
        fields = '__all__'


class CongViecSerializer(serializers.ModelSerializer):
    class Meta:
        model = CongViec
        fields = '__all__'


class PhongBanSerializer(serializers.ModelSerializer):
    ten_dia_diem = serializers.CharField(source='id_dia_diem.thanh_pho', read_only=True)
    
    class Meta:
        model = PhongBan
        fields = '__all__'


class NguoiPhuThuocSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiPhuThuoc
        fields = '__all__'


class NhanVienSerializer(serializers.ModelSerializer):
    ten_cong_viec = serializers.CharField(source='id_cong_viec.ten_cong_viec', read_only=True)
    ten_phong_ban = serializers.CharField(source='id_phong_ban.ten_phong_ban', read_only=True)
    ten_quan_ly = serializers.SerializerMethodField()
    nguoi_phu_thuoc = NguoiPhuThuocSerializer(many=True, read_only=True, source='nguoiphuthuoc_set')
    
    class Meta:
        model = NhanVien
        fields = '__all__'
    
    def get_ten_quan_ly(self, obj):
        if obj.id_quan_ly:
            return f"{obj.id_quan_ly.ho} {obj.id_quan_ly.ten}"
        return None


class NhanVienDetailSerializer(serializers.ModelSerializer):
    ten_cong_viec = serializers.CharField(source='id_cong_viec.ten_cong_viec', read_only=True)
    ten_phong_ban = serializers.CharField(source='id_phong_ban.ten_phong_ban', read_only=True)
    ten_quan_ly = serializers.SerializerMethodField()
    nguoi_phu_thuoc = NguoiPhuThuocSerializer(many=True, read_only=True, source='nguoiphuthuoc_set')
    
    class Meta:
        model = NhanVien
        fields = '__all__'
    
    def get_ten_quan_ly(self, obj):
        if obj.id_quan_ly:
            return f"{obj.id_quan_ly.ho} {obj.id_quan_ly.ten}"
        return None


class AttendanceSerializer(serializers.ModelSerializer):
    ten_nhan_vien = serializers.CharField(source='id_nhan_vien.ho', read_only=True)
    ho_ten_nhan_vien = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = '__all__'
    
    def get_ho_ten_nhan_vien(self, obj):
        return f"{obj.id_nhan_vien.ho} {obj.id_nhan_vien.ten}"


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id_nhan_vien', 'check_in', 'check_out']


class PayrollRecordSerializer(serializers.ModelSerializer):
    ten_nhan_vien = serializers.CharField(source='id_nhan_vien.ho', read_only=True)
    ho_ten_nhan_vien = serializers.SerializerMethodField()
    luong_co_ban = serializers.DecimalField(source='id_nhan_vien.luong', read_only=True, max_digits=12, decimal_places=2)
    tong_ngay_lam = serializers.DecimalField(max_digits=6, decimal_places=2)
    luong_thuc_nhan = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        model = PayrollRecord
        fields = '__all__'
    
    def get_ho_ten_nhan_vien(self, obj):
        return f"{obj.id_nhan_vien.ho} {obj.id_nhan_vien.ten}"


class PayrollCalculationSerializer(serializers.Serializer):
    thang = serializers.DateField(help_text="Ngày đầu tháng (VD: 2024-01-01)")
    id_nhan_vien = serializers.IntegerField(required=False, help_text="ID nhân viên cụ thể (nếu không có sẽ tính cho tất cả)") 