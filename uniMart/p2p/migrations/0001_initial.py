# Generated by Django 5.1.8 on 2025-04-04 15:15

import django.contrib.postgres.search
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import p2p.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hubs', '0004_alter_hub_updated_at'),
        ('utils', '0008_alter_category_service_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('condition', models.CharField(choices=[('new', 'New'), ('like_new', 'Like New'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], default='good', max_length=10)),
                ('status', models.CharField(choices=[('available', 'Available'), ('reserved', 'Reserved'), ('sold', 'Sold')], default='available', max_length=10)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('pickup_location', models.CharField(blank=True, max_length=200)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('meta_keywords', models.CharField(blank=True, help_text='Comma delimited set of SEO keywords for meta tag', max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, help_text='Content for description meta tag', max_length=255, null=True)),
                ('category', models.ForeignKey(blank=True, limit_choices_to={'service_type': 'p2p'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='p2p', to='utils.category')),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hubs.hub')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listed_products', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='utils.tag')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ImageField(default='p2p/default.jpg', upload_to=p2p.models.rename)),
                ('is_thumbnail', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='p2p.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('is_active', models.BooleanField(default=True)),
                ('offered_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('message', models.TextField(blank=True, max_length=500)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_requests', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='p2p.product')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('is_active', models.BooleanField(default=True)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('completed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('buyer_rating', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('seller_rating', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('buyer_feedback', models.TextField(blank=True, max_length=500)),
                ('seller_feedback', models.TextField(blank=True, max_length=500)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='transaction', to='p2p.product')),
                ('purchase_request', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='transaction', to='p2p.purchaserequest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['status', 'created_at'], name='p2p_product_status_0fd80a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='purchaserequest',
            unique_together={('product', 'buyer')},
        ),
    ]
