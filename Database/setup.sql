create database railway_miniproject character set utf8;
create user django_railways identified by "railways";
grant all on railway_miniproject.* to "django_railways"@"%";
flush privileges;