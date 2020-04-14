import scrapy
from bella.items import BellaItem
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose


class NewPaperItemLoader(ItemLoader):
    default_item_class = BellaItem
    clean_text = Compose(MapCompose(lambda v: v.strip()), Join())
    to_int = Compose(TakeFirst(), int)
    url_out = Join()
    public_date_out = Join()
    title_out = clean_text
    sapo_out = clean_text
    content_out = clean_text


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    # allowed_domains = ['stylemagazine.vn']
    allowed_domains = ['gaixinh2k.com']

    def start_requests(self):
        # urls = ['https://beta.dantri.com.vn/su-kien.htm', 'https://beta.dantri.com.vn/xa-hoi.htm', 'https://beta.dantri.com.vn/the-gioi.htm',
        #         'https://beta.dantri.com.vn/the-thao.htm', 'https://beta.dantri.com.vn/giao-duc-khuyen-hoc.htm', 'https://beta.dantri.com.vn/tam-long-nhan-ai.htm',
        #         'https://beta.dantri.com.vn/kinh-doanh.htm', 'https://beta.dantri.com.vn/bat-dong-san.htm', 'https://beta.dantri.com.vn/van-hoa.htm',
        #         'https://beta.dantri.com.vn/giai-tri.htm', 'https://beta.dantri.com.vn/phap-luat.htm', 'https://beta.dantri.com.vn/nhip-song-tre.htm',
        #         'https://beta.dantri.com.vn/suc-khoe.htm', 'https://beta.dantri.com.vn/suc-manh-so.htm', 'https://beta.dantri.com.vn/o-to-xe-may.htm',
        #         'https://beta.dantri.com.vn/tinh-yeu-gioi-tinh.htm']
        # urls = ['https://stylemagazine.vn/chuyen-muc/lam-dep/',
        # 'https://stylemagazine.vn/chuyen-muc/phong-cach-song/',
        # 'https://stylemagazine.vn/chuyen-muc/van-hoa/',
        # 'https://stylemagazine.vn/chuyen-muc/cong-nghe/',
        # 'https://stylemagazine.vn/chuyen-muc/su-kien/']
        # for url in urls:
        #     yield scrapy.Request(url, self.parse_page)
        url = 'https://gaixinh2k.com/'
        yield scrapy.Request(url, self.parse_page)

    def parse_page(self, response):
        yield scrapy.Request('https://gaixinh2k.com/', self.parse_page,dont_filter=True)
        # for url in response.css('div:not(.tt-border-block) div.tt-post.post.type-6 div.tt-post-info > a.tt-post-title::attr("href")').extract():
        #     yield scrapy.Request(url, self.parse_content)
        # next_page = response.css(
        #     "ul.page-numbers li a.next.page-numbers ::attr('href')").extract_first()
        # if next_page:
        #     url = next_page
        #     yield scrapy.Request(url, self.parse_page)

    def parse_content(self, response):
        my_loader = NewPaperItemLoader()    
        title = response.css(
            'article h1::text').extract_first().strip()
        my_loader.add_value('title', title)
        content = response.css(
            'article div.simple-text >  h4::text,div.simple-text > p:not(:first-child)::text,div.simple-text > p:not(:first-child) > *::text').extract()
        my_loader.add_value('content', content)
        image = list(
            {
                'image_url': img.css('img::attr(src)').extract_first(),
                'image_decription': img.css('p.wp-caption-text::text,p.wp-caption-text *::text').extract_first()
            } for img in response.css(
                'div.tt-content div.wp-caption')
        )

        for img in response.css('div.tt-content > *:not(div.wp-caption) img::attr(src)').extract():
            image.append({
                'image_url': img,
                'image_decription': None
            })
        my_loader.add_value('image', image)
        sapo = response.css(
            'article div.simple-text  p:first-child *::text').extract_first()
        my_loader.add_value('sapo', sapo)
        tag = response.css('ul.tt-tags li a::text').extract()
        my_loader.add_value('tag', tag)
        category = response.css(
            'div.tt-blog-category a::text').extract()
        my_loader.add_value('category', category)
        public_date = response.css(
            'span.tt-post-date-single::text').extract_first()
        my_loader.add_value('public_date', public_date)
        url = response.url
        my_loader.add_value('url', url)
        yield my_loader.load_item()
