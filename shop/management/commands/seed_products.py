from django.core.management.base import BaseCommand
from shop.models import Product
from django.core.files import File
from pathlib import Path

class Command(BaseCommand):
    help = '商品モデルにダミーデータを追加します'

    def handle(self, *args, **kwargs):
        BASE = Path('images')
        products = [
            {'name': '有機栽培トマト', 'description': '無農薬で育てた甘くてジューシーなトマト。ビタミンCたっぷりで美容にも効果的。', 'price': 1200, 'stock': 50, 'image': BASE / 'lily-banse--YHSwy6uqvk-unsplash.jpg'},
            {'name': '地元産ブロッコリー', 'description': '新鮮な地元産ブロッコリー。抗酸化作用が高く、免疫力アップに効果的。', 'price': 800, 'stock': 30, 'image': BASE / 'odiseo-castrejon-1CsaVdwfIew-unsplash.jpg'},
            {'name': '無農薬キャベツ', 'description': '農薬を使わずに育てた甘いキャベツ。食物繊維が豊富で腸内環境を整えます。', 'price': 600, 'stock': 20, 'image': BASE / 'odiseo-castrejon-1SPu0KT-Ejg-unsplash.jpg'},
            {'name': '有機ニンジン', 'description': 'β-カロテンたっぷりの有機栽培ニンジン。目と肌の健康に効果的。', 'price': 500, 'stock': 40, 'image': BASE / 'eiliv-aceron-ZuIDLSz3XLg-unsplash.jpg'},
            {'name': '地産地消セット', 'description': '地元の新鮮野菜を厳選したセット。栄養バランス抜群で家族の健康をサポート。', 'price': 2500, 'stock': 15, 'image': BASE / 'joseph-gonzalez-fdlZBWIP0aM-unsplash.jpg'},
        ]
        for p in products:
            obj, created = Product.objects.get_or_create(name=p['name'], defaults={k: v for k, v in p.items() if k != 'image'})
            if created and p.get('image') and p['image'].exists():
                with open(p['image'], 'rb') as img_file:
                    obj.image.save(p['image'].name, File(img_file), save=True)
        self.stdout.write(self.style.SUCCESS('ダミー商品データと画像を追加しました')) 