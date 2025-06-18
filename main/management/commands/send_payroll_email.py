from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from main.models import PayrollRecord
from datetime import datetime

class Command(BaseCommand):
    help = 'Gửi email bảng lương cho nhân viên'

    def add_arguments(self, parser):
        parser.add_argument('--month', type=str, help='Tháng cần gửi (MM/YYYY)')
        parser.add_argument('--test_email', type=str, help='Email test (mặc định: hokhanhduong9204@gmail.com)')

    def handle(self, *args, **options):
        # Parse tháng
        if options['month']:
            month = datetime.strptime(options['month'], '%m/%Y').date()
        else:
            # Mặc định là tháng hiện tại
            now = datetime.now()
            month = datetime(now.year, now.month, 1).date()

        # Email test
        test_email = options['test_email'] or 'hokhanhduong9204@gmail.com'

        # Lấy dữ liệu bảng lương
        payrolls = PayrollRecord.objects.select_related('id_nhan_vien').filter(
            thang__year=month.year,
            thang__month=month.month
        )

        # Gửi email cho từng nhân viên
        for payroll in payrolls:
            # Context cho template
            context = {
                'ho_ten': f"{payroll.id_nhan_vien.ho} {payroll.id_nhan_vien.ten}",
                'thang': month.strftime('%m/%Y'),
                'tong_ngay_lam': f"{payroll.tong_ngay_lam:.2f}",
                'luong_thuc_nhan': f"{payroll.luong_thuc_nhan:,.0f}"
            }

            # Tạo nội dung email
            html_content = render_to_string('email/payroll.html', context)

            # Tạo email
            email = EmailMessage(
                subject=f'Bảng lương tháng {month.strftime("%m-%Y")}',
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[test_email],  # Trong thực tế: payroll.id_nhan_vien.email
            )
            email.content_subtype = "html"  # Set để gửi dạng HTML

            try:
                email.send()
                self.stdout.write(
                    self.style.SUCCESS(f'Đã gửi email bảng lương cho {context["ho_ten"]}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Lỗi gửi email cho {context["ho_ten"]}: {str(e)}')
                ) 