This directory contains a dump of the HTML files from the [PlayStation DataCenter](https://psxdatacenter.com/) so I could avoid bombarding their server with requests when I scrape metadata.

```bash
wget -r -np -R "index.html*" https://psxdatacenter.com/games/
zip -9 -r psxdatacenter_dump.zip psxdatacenter.com
```
