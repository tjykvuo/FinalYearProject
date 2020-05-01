import django.dispatch

upload_csv = django.dispatch.Signal(providing_args=["user", "csv_file_list"])