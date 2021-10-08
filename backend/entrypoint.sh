#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --no-input
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate --no-input
echo "from django.contrib.auth.models import User, Group, Permission;
from django.contrib.contenttypes.models import ContentType;
from thumbimages.models import ThumbImage;
User.objects.filter(email='$DJANGO_ADMIN_EMAIL').delete();
User.objects.create_superuser('$DJANGO_ADMIN_USER', '$DJANGO_ADMIN_EMAIL', '$DJANGO_ADMIN_PASSWORD')
basic, created = Group.objects.get_or_create(name='basic');
ct = ContentType.objects.get_for_model(ThumbImage);
permission = Permission.objects.get(codename='hide_image', content_type=ct);
basic.permissions.add(permission);
permission = Permission.objects.get(codename='hide_image_medium', content_type=ct);
basic.permissions.add(permission);
permission = Permission.objects.get(codename='hide_image_link', content_type=ct);
basic.permissions.add(permission);
premium, created = Group.objects.get_or_create(name='premium');
permission = Permission.objects.get(codename='hide_image_link', content_type=ct);
premium.permissions.add(permission);
enterprise, created = Group.objects.get_or_create(name='enterprise');
user=User.objects.create_user('$DJANGO_BASIC_USER', password='$DJANGO_BASIC_PASSWORD');
user.is_superuser=False;
user.is_staff=False;
user.save();
basicgroup = Group.objects.get(name='basic');
user.groups.add(basicgroup);
user=User.objects.create_user('$DJANGO_PREMIUM_USER', password='$DJANGO_PREMIUM_PASSWORD');
user.is_superuser=False;
user.is_staff=False;
user.save();
premiumgroup = Group.objects.get(name='premium');
user.groups.add(premiumgroup);
user=User.objects.create_user('$DJANGO_ENTERPRISE_USER', password='$DJANGO_ENTERPRISE_PASSWORD');
user.is_superuser=False;
user.is_staff=False;
user.save();
enterprisegroup = Group.objects.get(name='enterprise');
user.groups.add(enterprisegroup);
" | python manage.py shell

exec "$@"