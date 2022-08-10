## Скрипты для автоматической генерации конфига

Скрипт add_device_and_configuration.py создаёт device в netbox и заливает конфиг на железки, 
на вход принимает 4 параметра:
- имя микротика в формате mkt.cli.sto.xxxx , где xxxx - город или улица: mkt.cli.sto.test.example
- белый ip адрес филиала: xxx.yyy.zzz.www
- шлюз филиала: xxx.yyy.zzz.www
- серая сеть филиала: xxx.yyy.zzz.www/mask

Скрипт add_reserved_tunnel.py генерирует конфиг для резервной сессии, принимает на вход следующие параметры
- имя микротика в формате mkt.cli.sto.xxxx , где xxxx - город или улица: mkt.cli.sto.test.example
- белый ip адрес филиала: xxx.yyy.zzz.www
- шлюз филиала: xxx.yyy.zzz.www
