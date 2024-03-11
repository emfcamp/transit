from django.core.management.base import BaseCommand
import darwin.tasks


class Command(BaseCommand):
    help = "Downloads the latest timetable and reference files from Darwin"

    def handle(self, *args, **options):
        s3_client = darwin.tasks.get_s3_client()

        files = s3_client.list_objects_v2(
            Bucket=darwin.tasks.TT_BUCKET,
            Prefix=darwin.tasks.FILE_PREFIX,
        )

        tt = []
        tt_ref = []
        for file in files["Contents"]:
            file_name = file["Key"].removeprefix(darwin.tasks.FILE_PREFIX)
            if match := darwin.tasks.TT_RE.match(file_name):
                tt.append(((int(match["year"]), int(match["month"]), int(match["day"])), file_name))
            elif match := darwin.tasks.TT_REF_RE.match(file_name):
                tt_ref.append(((int(match["year"]), int(match["month"]), int(match["day"])), file_name))

        tt.sort(reverse=True, key=lambda x: x[0])
        tt_ref.sort(reverse=True, key=lambda x: x[0])

        latest_tt = tt[0][1] if tt else None
        latest_tt_ref = tt_ref[0][1] if tt_ref else None

        if latest_tt:
            darwin.tasks.download_tt_file.delay(latest_tt)
        if latest_tt_ref:
            darwin.tasks.download_tt_ref_file.delay(latest_tt_ref)
