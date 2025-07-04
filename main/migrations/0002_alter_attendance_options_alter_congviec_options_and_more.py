# Generated by Django 5.0.14 on 2025-06-18 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['-ngay_lam'], 'verbose_name': 'Chấm công', 'verbose_name_plural': 'Chấm công'},
        ),
        migrations.AlterModelOptions(
            name='congviec',
            options={'verbose_name': 'Công việc', 'verbose_name_plural': 'Công việc'},
        ),
        migrations.AlterModelOptions(
            name='diadiem',
            options={'verbose_name': 'Địa điểm', 'verbose_name_plural': 'Địa điểm'},
        ),
        migrations.AlterModelOptions(
            name='khuvuc',
            options={'verbose_name': 'Khu vực', 'verbose_name_plural': 'Khu vực'},
        ),
        migrations.AlterModelOptions(
            name='nguoiphuthuoc',
            options={'verbose_name': 'Người phụ thuộc', 'verbose_name_plural': 'Người phụ thuộc'},
        ),
        migrations.AlterModelOptions(
            name='nhanvien',
            options={'verbose_name': 'Nhân viên', 'verbose_name_plural': 'Nhân viên'},
        ),
        migrations.AlterModelOptions(
            name='payrollrecord',
            options={'ordering': ['-thang'], 'verbose_name': 'Bảng lương', 'verbose_name_plural': 'Bảng lương'},
        ),
        migrations.AlterModelOptions(
            name='phongban',
            options={'verbose_name': 'Phòng ban', 'verbose_name_plural': 'Phòng ban'},
        ),
        migrations.AlterModelOptions(
            name='quocgia',
            options={'verbose_name': 'Quốc gia', 'verbose_name_plural': 'Quốc gia'},
        ),
        migrations.AlterField(
            model_name='nhanvien',
            name='luong',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='payrollrecord',
            name='luong_thuc_nhan',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
