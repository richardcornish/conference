from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'search', 'sms', 'voice', 'about']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static': StaticViewSitemap,
}
