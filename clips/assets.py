from django_assets import Bundle, register
from django_assets.filter import Filter, register_filter
import subprocess


class TailwindFilter(Filter):
    name = "tailwind"

    def input(self, _in, out, **kwargs):
        p = subprocess.Popen(
            ["tailwindcss", "-i", "-", "--minify"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = p.communicate(input=_in.read().encode("utf-8"))
        out.write(stdout.decode("utf-8"))
        print(stderr.decode("utf-8"))


register_filter(TailwindFilter)


tailwind = Bundle("tailwind.css", output="main.css", filters="tailwind")
register("tailwind", tailwind)
