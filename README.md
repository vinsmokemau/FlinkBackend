# FlinkBackend
This repository is part of a technical test from Flink

## Run project


```sh
docker-compose -f local.yml build
docker-compose -f local.yml up
```

## Test project


```sh
docker-compose -f local.yml exec django python manage.py test apps.companies.tests
```

## Contact

Vinsmoke Mau – [@vinsmokemau](https://twitter.com/vinsmokemau) – mauricio.munguia@makingmex.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/vinsmokemau/FlinkBackend](https://github.com/vinsmokemau/FlinkBackend)

## Contributing

1. Create your feature branch (`git checkout -b feature/fooBar`)
2. Commit your changes (`git commit -am 'Add some fooBar'`)
3. Push to the branch (`git push origin feature/fooBar`)
4. Create a new Pull Request
