# Discount Code service

## How to run

### Development
1. Install packages using `requirements-dev.txt`.
2. Setup pre-commit hooks with
```bash
$ pre-commit install
$ pre-commit install --hook-type commit-msg
```
3. Prepare the db
```bash
$ python manage.py migrate
```
4. Run the server
```bash
$ python manage.py runserver
```

### Production
- TBA


## Demo

1. Run the programme.
2. Goto `<base-url>/swagger` for swagger documentation and to play with API developed.
3. Run the GET endpoint `/codes/generate/{count}` to mimic the effort of the scheduler. This will generate buffer discount code list.
4. Run the POST endpoint `/codes/` to set given number of codes to the given brand.
5. Run the GET endpoint `/codes/discountcode/{brand}` to get an available discount code for the given brand.
