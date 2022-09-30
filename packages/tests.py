from datetime import datetime

from django.test import TestCase

from packages.models import Package


class PackageTestCase(TestCase):
    def test_creates_and_save_package_from_dict_data(self):
        package = {
            "name": "quakerheritage",
            "author": "",
            "author_email": "",
            "description": "# quakerHeritage\nProject to support the collation of PDF data on the Quaker Meeting House Heritage Project into a database\n\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)\n![status](https://img.shields.io/badge/status-released-green)\n\n## Dependencies\n\n### Required Python Libaries\n* bs4\n* csv\n* io\n* numpy\n* pandas\n* pdfplumber\n* re\n* requests\n* urllib3\n\n### Disclaimer\n\nThis project has been specifically coded for the Quaker Meeting House Heritage Project, both in hard-coded variables, and hard-coded parameters for extracting text. It is a tool to suit a very specific use-case and may not work if used otherwise. The project further depends on the files required being listed online at the URLs provided. If Britain Yearly Meeting takes down the website and associated pdfs, back-ups are available on the Internet Archive's Wayback Machine. The code can also be adapted to work with locally downloaded pdfs. go to Appendix: Hosting Errors to note the required changes. \n\n## Contributing\n\nFeedback is both welcome and encouraged. If you use the code, or just find issues while browsing, please report them by [clicking here.](github.com/aclayden/quakerHeritage/issues)\n\n## Licence\n\nDistributed under [AGPL version 3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)\n\n## Contact\n\nFor queries please reach out via GitHub by either raising an issue or contacting me directly. https://github.com/aclayden\n",
            "keywords": "",
            "version": "0.0.2",
            "maintainer": "",
            "maintainer_email": "",
        }
        p = Package(**package)
        p.save()

        for key in package.keys():
            assert getattr(p, key) == package[key]

        assert Package.objects.count() == 1
